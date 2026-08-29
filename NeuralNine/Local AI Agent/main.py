import os
import json
from typing import TypedDict

from dotenv import load_dotenv
from imap_tools import MailBox, AND

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END


# Load environment variables from the .env file
load_dotenv()


# IMAP configuration
# These values should be defined in the .env file
IMAP_HOST = os.getenv('IMAP_HOST')
IMAP_USER = os.getenv('IMAP_USER')
IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
IMAP_FOLDER = 'INBOX'


# Name of the LLM model used by the application
CHAT_MODEL = 'qwen3.5:9b'


class ChatState(TypedDict):
    # Stores the conversation history between the user, LLM and tools
    messages: list


def connect():
    """
    Create and authenticate an IMAP mailbox connection.
    The connection starts in the configured folder.
    """

    # Create a connection to the IMAP server
    mail_box = MailBox(IMAP_HOST)

    # Authenticate using the credentials from the environment
    mail_box.login(
        IMAP_USER,
        IMAP_PASSWORD,
        initial_folder=IMAP_FOLDER
    )

    return mail_box


@tool
def list_unread_emails():
    """
    Return a list of every unread email with its UID,
    subject, date and sender.
    """

    print('List Unread Emails Tool Called')

    # Open the mailbox connection.
    # The "with" statement automatically closes the connection afterwards.
    with connect() as mb:

        # Search for emails that have not been marked as read.
        # headers_only=True avoids downloading the entire email body.
        # mark_seen=False makes sure we don't mark emails as read.
        unread = list(
            mb.fetch(
                criteria=AND(seen=False),
                headers_only=True,
                mark_seen=False
            )
        )

    # Return a friendly message if there are no unread emails
    if not unread:
        return 'You have no unread messages.'

    # Convert the email information into JSON
    response = json.dumps([
        {
            'uid': mail.uid,
            'date': mail.date.astimezone().strftime('%Y-%m-%d %H:%M'),
            'subject': mail.subject,
            'sender': mail.from_
        }
        for mail in unread
    ])

    return response


@tool
def summarize_email(uid):
    """
    Summarize a single email using its IMAP UID.
    The result is returned as plain text.
    """

    print('Summarize E-Mail Tool Called on', uid)

    # Connect to the mailbox and retrieve the requested email
    with connect() as mb:

        # Search for an email matching the provided UID.
        # mark_seen=False prevents the email from being marked as read.
        mail = next(
            mb.fetch(
                AND(uid=uid),
                mark_seen=False
            ),
            None
        )

        # Handle the case where the email cannot be found
        if not mail:
            return f'Could not summarize e-mail with UID {uid}.'

        # Build a prompt containing the email information
        # and its body so the LLM can summarize it.
        prompt = (
            "Summarize this e-mail concisely:\n\n"
            f"Subject: {mail.subject}\n"
            f"Sender: {mail.from_}\n"
            f"Date: {mail.date}\n\n"
            f"{mail.text or mail.html}"
        )

        # Use the raw LLM because we don't want the model
        # to call any tools while summarizing an email.
        return raw_llm.invoke(prompt).content


# Create the main LLM.
# This model is responsible for deciding what action to take.
llm = init_chat_model(CHAT_MODEL, model_provider='ollama')

# Give the LLM access to our email-related tools.
# The model can decide when it needs to call them.
llm = llm.bind_tools([
    list_unread_emails,
    summarize_email
])


# Create a second LLM without tools.
# This one is used only to summarize email content.
raw_llm = init_chat_model(CHAT_MODEL, model_provider='ollama')


def llm_node(state):
    """
    Run the LLM using the current conversation state.
    """

    # Send the conversation history to the LLM
    response = llm.invoke(state['messages'])

    # Add the LLM response to the conversation history
    return {'messages': state['messages'] + [response]}


def router(state):
    """
    Decide what should happen after the LLM responds.

    If the LLM requested a tool call, route the graph to the
    tools node. Otherwise, finish the conversation.
    """

    # Get the most recent message produced by the LLM
    last_message = state['messages'][-1]

    # Check whether the LLM requested any tool calls
    return 'tools' if getattr(last_message, 'tool_calls', None) else 'end'


# ToolNode is responsible for executing the tools
# requested by the LLM.
tool_node = ToolNode([
    list_unread_emails,
    summarize_email
])


def tools_node(state):
    """
    Execute the tools requested by the LLM
    and add their results to the conversation.
    """

    # Execute the requested tool calls
    result = tool_node.invoke(state)

    # Add the tool results to the existing conversation
    return {
        'messages': state['messages'] + result['messages']
    }


# Create the LangGraph state machine
builder = StateGraph(ChatState)


# Register the nodes used by the graph
builder.add_node('llm', llm_node)
builder.add_node('tools', tools_node)


# The conversation starts by calling the LLM
builder.add_edge(START, 'llm')


# After a tool has been executed, send the result back to the LLM.
# This allows the LLM to interpret the tool result and respond
# naturally to the user.
builder.add_edge('tools', 'llm')


# After the LLM responds, use the router to decide whether
# we need to call a tool or finish the conversation.
builder.add_conditional_edges(
    'llm',
    router,
    {
        'tools': 'tools',
        'end': END
    }
)


# Compile the graph into an executable application
graph = builder.compile()


if __name__ == '__main__':

    # Start with an empty conversation
    state = {'messages': []}

    print('Type an instruction or "quit".\n')

    while True:

        # Read the user's instruction from the terminal
        user_message = input('> ')

        # Exit the application when the user types "quit"
        if user_message.lower() == 'quit':
            break

        # Add the user's message to the conversation history
        state['messages'].append({
            'role': 'user',
            'content': user_message
        })

        # Run the LangGraph.
        # The LLM may call tools, receive their results,
        # and then generate the final answer.
        state = graph.invoke(state)

        # Display the latest message produced by the graph
        print(state['messages'][-1].content, '\n')
