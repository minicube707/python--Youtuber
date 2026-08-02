from fastmcp import FastMCP
import math

# Create a new MCP server named "Math".
# This server will expose tools that can be called by an MCP client.
mcp = FastMCP("Math")


# Register this function as an MCP tool.
# The language model can call this function when it needs to add two numbers.
@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Register this function as an MCP tool.
# The language model can call this function when it needs to add two numbers.
@mcp.tool
def sub(a: int, b: int) -> int:
    """Sub two numbers"""
    return a - b


# Register this function as an MCP tool.
# The language model can call this function to multiply two numbers.
@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


# Register this function as an MCP tool.
# The language model can call this function to divide two numbers.
@mcp.tool
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("The divisor cannot be zero.")
    return a / b


# Register this function as an MCP tool.
# The language model can call this function to know if a number is prime
@mcp.tool
def is_prime(n: int) -> bool:
    """Return True if the number is prime, else False"""
    
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0: return False
    return True


# Register this function as an MCP tool.
# The language model can call this function to give the square root of a number
@mcp.tool
def sqrt(a: int) -> float:
    """Give the square root of a number"""
    return math.sqrt(a)


# Register this function as an MCP tool.
# The language model can call this function to give the digit of PI
@mcp.tool()
def get_pi() -> float:
    """Return the number PI"""
    return math.pi


# Register this function as an MCP tool.
# The language model can call this function to compute the prime factorization of a positive integer.
@mcp.tool()
def prime_factorization(n: int) -> list[int]:
    """
    Compute the prime factorization of a positive integer.

    Args:
        n: A positive integer greater than 1.

    Returns:
        list[int]: A list of the prime factors of ``n``, including repeated factors.
    """
    if n < 2:
        raise ValueError("n must be greater than 1.")

    factors = []

    # Factor out powers of 2.
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Factor out odd divisors.
    divisor = 3
    while divisor <= math.isqrt(n):
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2

    # If n is still greater than 1, it is prime.
    if n > 1:
        factors.append(n)

    return factors


# Start the MCP server when this file is executed directly.
# The server will wait for incoming requests from MCP clients.
if __name__ == "__main__":
    mcp.run()