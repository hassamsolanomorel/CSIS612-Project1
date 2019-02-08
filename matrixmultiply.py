"""
Filename: newmatrixmultiply.py
Author(s): Hassam S
Multiplies two matricies and returns the result
"""
import numpy as np
import threading
# import multiprocessing
# from multiprocessing import Pool, Process
# from multiprocessing.sharedctypes import Value, Array
# from ctypes import Structure
import time
import sys


# class WorkPackage(Structure):
#     i = 0
#     j = 0
#     row = []
#     col = []
#
#     def __init__(self, i, j, row, col):
#         self.i = i
#         self.j = j
#         self.row = row
#         self.col = col


# class SharedMat(Structure):
#     matrix = [[]]
#
#     def __init__(self, size):
#         self.matrix = np.zeros((size, size), dtype=int)


def multiplyAndInsert(mat, i, j, row, col):

    sum = 0
    for k in range(len(row)):
        sum += row[k] * col[k]

    mat[i][j] = sum


def iterativeApproach(size: int):
    A = np.random.randint(-100,
                          high=100,
                          size=(size, size),
                          dtype=int)

    B = np.random.randint(-100,
                          high=100,
                          size=(size, size),
                          dtype=int)
    C = []  # final result
    start = time.time()
    for i in range(len(A)):
        row = []  # the new row in new matrix
        for j in range(len(B)):

            product = 0  # the new element in the new row
            for v in range(len(A[i])):
                product += A[i][v] * B[v][j]
            row.append(product)  # append sum of product into the new row

        C.append(row)  # append the new row into the final result

    stop = time.time()
    diff = stop - start
    print(f'Iterative Threads Time: %.0f minutes %.8f seconds' %
          (diff/60, diff % 60))


# def optimizedThreads(size: int):
#     A = np.random.randint(-100,
#                           high=100,
#                           size=(size, size),
#                           dtype=int)
#
#     B = np.random.randint(-100,
#                           high=100,
#                           size=(size, size),
#                           dtype=int)
#
#     shared_C = Value(SharedMat, size, lock=False)
#     work = []
#     workItems = 0
#     # start = time.time()
#     for i in range(len(A)):
#         # print(f'MAT-A ROW: {A[i,:]}')
#         for j in range(len(B)):
#             # print(f'MAT-B COL: {B[: ,j]}')
#             # print(f'i:{i}, j:{j}')
#             work_item = (shared_C, WorkPackage(i, j, A[i, :], B[:, j]))
#             work.append(work_item)
#             workItems += 1
#
#     print(f'Before:{shared_C.matrix}')
#
#     with Pool(processes=8) as pool:
#         # print(work)
#         start = time.time()
#         pool.imap_unordered(multiplyAndInsert, work)
#         stop = time.time()
#
#     print(f'After:{shared_C.matrix}')
#     diff = stop - start
#     print(f'Optimized Threads Time: %.0f minutes %.8f seconds' %
#           (diff/60, diff % 60))


def nativeThreads(size: int):
    A = np.random.randint(-100,
                          high=100,
                          size=(size, size),
                          dtype=int)

    B = np.random.randint(-100,
                          high=100,
                          size=(size, size),
                          dtype=int)

    C = np.empty((size, size), dtype=int)
    # print(f'MAT-A:\n{A}\n\n MAT-B:\n{B}')
    threads = []
    for i in range(len(A)):
        # print(f'MAT-A ROW: {A[i,:]}')
        for j in range(len(B)):
            # print(f'MAT-B COL: {B[: ,j]}')
            # print(f'i:{i}, j:{j}')
            thread = threading.Thread(target=multiplyAndInsert,
                                      args=(C, i, j,
                                            A[i, :],
                                            B[:, j]))
            threads.append(thread)

    start = time.time()
    for t in threads:
        t.start()

    for t in set(threads):
        t.join()

    stop = time.time()
    diff = stop - start
    print(f'Native Thread Time: %.0f minutes %.8f seconds' %
          (diff/60, diff % 60))


if __name__ == '__main__':
    size = int(sys.argv[1])
    print(f"Matrix Multiplication Execution Times. Size:{size}")
    print(20*'_')
    # print("Running 'OptimizedThreads'...")
    # optimizedThreads(size)
    print("\nRunning 'NativeThreads'...")
    nativeThreads(size)
    print("\nRunning 'IterativeThreads'...")
    iterativeApproach(size)
