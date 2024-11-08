---
layout: post
title: Multithreading and Multiprocessing in Python
date: 2030-01-01
description: Core concepts, distinctions, best practices, and potential implementations
tags: [concepts, code]
category: research
---

Python is a programming language not designed for high-performance applications, its benefits come from the ease of
learning and usability.
Even though there are several arrangements you can employ to speed up your applications.

In this blog post, I would like to show you what I have learnt regarding this topic and provide you some code and
reference that could be useful.

First of all, _functional programming_ is the most valuable aspect to take into account before applying whatever
multiprocessing-multithreading techniques.
Here, what I think are interesting resources to consider are provided:

- [Refactoring Book](https://refactoring.com/)
- [The Clean Coder's Blog](https://blog.cleancoder.com/)
- [Python documentation](https://docs.python.org/3/howto/functional.html)
- [RealPython Functional Programming](https://realpython.com/python-functional-programming/)

After evaluating your program using functional programming best practices, you can begin analyzing which tasks are
suitable for parallel execution and identifying any slower sections of the code.

It's important to note that if your code adheres to functional programming principles correctly, incorporating parallel
computation will be much easier.

Before we dive into the differences between multithreading and multiprocessing and how to choose between them,
let's first cover some foundational concepts to build the necessary background understanding.

#### Thread vs. Process

First of all, the thread is part of the process; moreover, a process can consist of multiple threads.

### Definitions

- _Process_: a process is an independent program in execution.
  It contains the program code, its current activity, and its allocated system resources, like memory and CPU time.

- _Thread_: a thread is the smallest unit of execution within a process.
  Multiple threads can exist within the same process, sharing the same memory space but able to execute
  independently.

### Memory usage

- _Process_: each process operates in its own memory space; the memory allocated to a process is isolated from other
  processes, which provides stability and security since one process cannot directly interfere with the memory of
  another process.

- _Thread_: threads with the same process share the same memory space. This allows them to access the same data more
  efficiently, but also introduces risks of conflicts if multiple threads try to modify the same data simultaneously.

### Communication

- _Process_: processes generally communicate with each other through inter-process communication (IPC) mechanisms like
  pipes, message queues, or shared memory, which can be relatively slow and complex to implement.

- _Thread_: since threads within the same process share the same memory, they can communicate directly by reading and
  writing to shared variables. This communication is faster and simpler than IPC between processes.

### Overhead

- _Process_: processes have a higher overhead compared to threads because creating, managing and switching between
  processes requires more resources. The operating system needs to maintain separate memory and resources for each
  process.

- _Thread_: threads have a lower overhead compared to processes. Creating and switching between threads within the same
  process is faster and requires fewer resources since they have the same memory space.

### Use Case

- _Process_: processes are typically used when tasks need to be isolated from each other, such as running different
  applications on a computer.

- _Thread_: threads are commonly used in situations where tasks are closely related and need to share data quickly and
  efficiently, such as in a web server handling multiple client requests concurrently.

### Summary

- **Isolation**: processes are isolated from each other, while threads within the same process are not
- **Resource Sharing**: threads share resources of the process they belong to, including memory and open files, while
  processes do not share their resources by default.
- **Creation and Context Switching**: creating and switching between processes is more resource-intensive than creating
  and switching between threads.

Useful links:

- [Mario](https://medium.com/capital-one-tech/python-guide-using-multiprocessing-versus-multithreading-55c4ea1788cd)
- [Mario](https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/)

#### Multi-threading vs. Multi-processing

Multi-threading and multi-processing are both techniques used to achieve parallelism and improve the performance of a
program by dividing tasks into smaller, concurrent units of execution. However, they differ in how they manage these
units and use system resources.

### Definitions

- _Multi-processing_: multi-processing involves running multiple processes simultaneously, each with its own independent
  memory space. These processes can run on separate CPU cores and do not share memory, which eliminates the need for
  synchronization but increases memory usage.

- _Multi-threading_: multi-threading involves threads within a single process sharing memory, leading to potential
  synchronization issues, while multi-processing uses separate memory spaces for each process,
  avoiding these issues but at the cost of higher memory usage and communication complexity.

### Memory usage

- _Multi-processing_: each process in a multi-processing environment has its own memory space, so processes do not share
  data directly. This isolation can be beneficial for preventing conflicts but can lead to higher memory consumption
  since each process must maintain its own memory.

- _Multi-threading_: since all threads within a multi-threaded application share the same memory space, they can easily
  access and modify shared data. However, this also means that multi-threading can lead to issues such as race
  conditions, where multiple threads try to modify the same data simultaneously, leading to inconsistent results.

### Communication

- _Multi-processing_: processes in a multi-processing setup typically communicate using IPC mechanisms. While secure and
  isolated, this communication is generally slower and more complex compared to the shared memory approach used in
  multi-threading.

- _Multi-threading_: threads in a multi-threading program communicate by accessing shared memory. This is efficient, but
  requires careful synchronization (e.g., using mutexes or locks) to avoid conflicts and ensure data integrity.

### Overhead

- _Multi-processing_: multi-processing has higher overhead than multi-threading because creating and managing separate
  processes requires more resources, including memory and CPU time for context switching between processes.

- _Multi-threading_: multi-threading generally has lower overhead compared to multi-processing because threads share
  resources and the operating system does not need to create a separate memory space for each thread. However, the
  need for synchronization mechanisms can introduce some complexity and performance penalties.

### Use case

- _Multi-processing_: multi-processing is ideal for tasks that require significant CPU computation and benefit from
  running in parallel without sharing memory, such as data processing, simulations, or applications that need to fully
  use multiple cores without worrying about synchronization issues

- _Multi-threading_: multi-threading is well-suited for applications that require concurrent execution of tasks that
  share data or resources, such as a web server that handles multiple requests simultaneously.

### Performance

- _Multi-processing_: multi-processing can achieve true parallelism, even in languages with a GIL (like Python), because
  each process runs in its own memory space. This made it suitable for CPU-bound tasks that require heavy computation
  across multiple cores.

- _Multi-threading_: multi-threading can provide significant performance improvements, especially on multi-core
  processors, but it is limited by the Global Interpreter Lock (GIL) in some languages like Python, which can prevent
  true parallel execution of threads.

### Summary

- _Memory sharing_: multi-threading involves threads within a single process sharing memory, leading to potential
  synchronization issues, while multi-processing uses separate memory spaces for each process, avoiding these issues
  but at the cost of higher memory usage and communication complexity.
- _Communication_: multi-threading uses shared memory for fast communication, while multi-processing relies on
  slower IPC mechanisms.
- _Overhead_: multi-threading has lower overhead in terms of memory and context switching, while multi-processing has
  higher overhead due to the need to manage separate processes.
- _Parallelism_: multi-processing can achieve true parallelism even in environments with limitations like the GIL, while
  multi-threading may be limited by such factors.
- _Overall_: multi-threading is typically used for tasks that require concurrent execution with shared resources, while
  multi-processing is preferred for tasks that benefit from true parallelism and isolation.

GLOBAL INTERPRETE LOCK (GIL):

- ensures thread safety
- improves single thread performance
- prevents simultaneous multi-threading: bad for cpu limited tasks
- I/O limited threads are hardly affected

PROCESS: an instance of a program (e.g. a Python interpreter)

- takes advantage of multiple CPUS and cores
- separate memory space -> memory is not shared between processes
- great for CPU-bound processing
- new process is started indipendently from other processes
- processes are interruptable/killable
- one GIL for each process -> avoids GIL limitation

- heavyweight
- starting a process is slower than starting a thread
- more memory
- IPC (inter-process communication) is more complicated

THREAD: an entity within a process that can be scheduled (also
known as "lightweight process")

- all threads within within a process share the same memory
- lightweight
- starting a thread is faster than starting a process
- great for I/O bound tasks

- threading is limited by GIL: only one thread at a time
- no effect for CPU-bound tasks
- not interruptable/killable
- careful with race conditions

GIL:

- a lock that allows only one thread at a time to execute in Python
- needed in CPython because memory management is not thread-safe
- Avoid:
  - use multiprocessing
  - use a different, free-threaded Python implementation (Jython, IronPython)
  - use Python as a wrapper for third-party libraries (C/C++) -> numpy, scipy

#### Multi-threading vs. Multi-processing in Python

### Multi-threading

get maximum number of threads

in the same process, threads are not executed simultaneously

threading -> I/O bound tasks
multiprocessing -> CPU limited tasks

Threading:

- a new thread is spawned within the existing process
- starting a thread is faster than starting a process
- memory often necessary to control access to shared data
- one GIL (Global Interpreter Lock) for all threads

Multiprocessing:

- a new process is started independent from the first process
- starting a process is slower than starting a thread
- memory is not shared between processes
- mutexes not necessary (unless threading in the new process)
- one GIL (Global Interpreter Lock) for each process

https://stackoverflow.com/questions/16710849/what-is-the-maximum-number-of-threads-a-process-can-have-in-windows
https://stackoverflow.com/questions/344203/maximum-number-of-threads-per-process-in-linux
https://learn.microsoft.com/en-us/windows/win32/procthread/thread-stack-size
https://medium.com/@mehta.kavisha/different-methods-of-multiprocessing-in-python-70eb4009a990
https://www.youtube.com/watch?v=AZnGRKFUU0c

```python
import psutil
import platform
import resource

# Get the operating system name
os_name = platform.system()

# Get total virtual memory in bytes
total_virtual_memory = psutil.virtual_memory().total
print(f"Total Virtual Memory: {total_virtual_memory} bytes")

# Determine stack size based on the operating system
if os_name == "Linux":
    import resource
    # Get stack size in bytes on Linux
    stack_size = resource.getrlimit(resource.RLIMIT_STACK)[0]
else:
    # Default to 1 MB for non-Linux systems
    stack_size = 1 * 1024 * 1024  # 1 MB in bytes

# Convert stack size to MB for consistency
stack_size_mb = stack_size / (1024 * 1024)
print(f"Stack Size: {stack_size_mb} MB")

# Calculate the max number of threads
max_n_threads = total_virtual_memory / (stack_size * 1024 * 1024)
print(f"Max number of threads for process: {max_n_threads}")
```

thread starvation

### Multi-processing

get maximum number of threads:

60 in linux

```python

import os
import multiprocessing

n_cpu = os.cpu_count()
n_cpu = multiprocessing.cpu_count()
```

---
