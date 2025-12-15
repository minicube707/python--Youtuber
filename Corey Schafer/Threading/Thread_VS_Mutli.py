import time, os
from threading import Thread, current_thread
from multiprocessing import Process, current_process


COUNT = 200000000
SLEEP = 5

def normal_code_sleep(SLEEP):

    start = time.time()
    io_bound(SLEEP)
    io_bound(SLEEP)

    end = time.time()
    print('Time taken in seconds -', end - start)

def threading_code_sleep(SLEEP):
	
    start = time.time()
	
    #Initialisation of  threading
    t1 = Thread(target = io_bound, args =(SLEEP, ))
    t2 = Thread(target = io_bound, args =(SLEEP, )) 
	
    #Read the code
    t1.start()
    t2.start()  
	
    # Wait for the thread to complete 
    t1.join()
    t2.join()   
    end = time.time()
	
    print('Time taken in seconds -', end - start)


def normal_code_count(COUNT):

    start = time.time()
    cpu_bound(COUNT)
    cpu_bound(COUNT)

    end = time.time()
    print('Time taken in seconds -', end - start)

def threading_code_count(COUNT):
	
    start = time.time()
	
    #Initialisation of  threading
    t1 = Thread(target = cpu_bound, args =(COUNT, ))
    t2 = Thread(target = cpu_bound, args =(COUNT, )) 
	
    #Read the code
    t1.start()
    t2.start()  
	
    # Wait for the thread to complete 
    t1.join()
    t2.join()   
    end = time.time()
	
    print('Time taken in seconds -', end - start)

def processing_code_count(COUNT):
	
    start = time.time()
	
    #Initialisation of  threading
    p1 = Process(target = cpu_bound, args =(COUNT, ))
    p2 = Process(target = cpu_bound, args =(COUNT, ))
	
    #Read the code
    p1.start()
    p2.start() 
	
    # Wait for the thread to complete 
    p1.join()
    p2.join()   
    end = time.time()
	
    print('Time taken in seconds -', end - start)

def io_bound(sec):

	pid = os.getpid()
	threadName = current_thread().name
	processName = current_process().name

	print(f"{pid} * {processName} * {threadName} \
		---> Start sleeping...")
	time.sleep(sec)
	print(f"{pid} * {processName} * {threadName} \
		---> Finished sleeping...")

def cpu_bound(n):

	pid = os.getpid()
	threadName = current_thread().name
	processName = current_process().name

	print(f"{pid} * {processName} * {threadName} \
		---> Start counting...")

	while n>0:
		n -= 1

	print(f"{pid} * {processName} * {threadName} \
		---> Finished counting...")


def main(SLEEP, COUNT):
    
    #Part 1
    print("")
    print("SLEEP")
    normal_code_sleep(SLEEP)
    print("")
    threading_code_sleep(SLEEP)
    
    #Commentaire
    #Le multithreading est la solution idéale pour exécuter des tâches dans lesquelles le temps d'inactivité de notre processeur peut être utilisé pour effectuer d'autres tâches.
    #Ainsi, gagner du temps en exploitant le temps d’attente. 

    #Part 2
    print("")
    print("COUNT")
    normal_code_count(COUNT)
    print("")
    threading_code_count(COUNT)

    #Commentaire
    #lorsque Thread-1 a démarré, il a acquis le Global Interpreter Lock (GIL) qui a empêché Thread-2 d'utiliser le processeur.
    #Par conséquent, Thread-2 a dû attendre que Thread-1 termine sa tâche et libère le verrou afin de pouvoir acquérir le verrou et effectuer sa tâche.
    #Cette acquisition et cette libération du verrou ont ajouté une surcharge au temps d'exécution total.
    #Par conséquent, nous pouvons affirmer avec certitude que le threading n’est pas une solution idéale pour les tâches qui nécessitent que le processeur fonctionne sur quelque chose. 

    #Part 3
    print("")
    print("COUNT")
    normal_code_count(COUNT)
    print("")
    processing_code_count(COUNT)

if __name__=="__main__":

    main(SLEEP, COUNT)
	
    
	
