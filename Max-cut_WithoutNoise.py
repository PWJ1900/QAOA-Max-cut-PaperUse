import time
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
from qiskit.providers.aer import AerSimulator
edges = [[0, 1], [1, 2], [2, 3], [3, 0]]
# 初始化minimize里面list的长度n/2为其p迭代次数
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit import Aer, execute
nqubits = 4


def maxcut_obj(x):
    obj = 0
    for i, j in edges:
        if x[i] != x[j]:
            obj -= 1
    return obj


def compute_expectation(counts):
    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        obj = maxcut_obj(bitstring)
        avg += obj * count
        sum_count += count
    print(avg)
    return avg / sum_count

#==============================================================
"""初始电路为：
# def create_qaoa_circ(theta):
#     nqubits = 4
#     p = len(theta) // 2  # number of alternating unitaries
#     qc = QuantumCircuit(nqubits)
#     beta = theta[:p]
#     gamma = theta[p:]
#     # initial_state
#     for i in range(0, nqubits):
#         qc.h(i)
#     for irep in range(0, p):
#             qc.cx(pair[0], pair[1])
#             qc.rz(2 * gamma[irep], qubit=pair[1])
#             qc.cx(pair[0], pair[1])
#         # mixer unitary
#         for i in range(0, nqubits):
#             qc.rx(2 * beta[irep], i)
#     qc.measure_all()
#     return qc
   """
# =================================================================
"""深度优先搜索电路为：
# def create_qaoa_circ(theta):
#     nqubits = 4
#     p = len(theta) // 2  # number of alternating unitaries
#     qc = QuantumCircuit(nqubits)
#     beta = theta[:p]
#     gamma = theta[p:]
#     # initial_state
#     for i in range(0, nqubits):
#         qc.h(i)
#     for irep in range(0, p):
#             qc.cx(pair[0], pair[1])
#             qc.rz(2 * gamma[irep], qubit=pair[1])
#             qc.cx(pair[0], pair[1])
#         # mixer unitary
#         for i in range(0, nqubits):
#             qc.rx(2 * beta[irep], i)
#     qc.measure_all()
#     return qc
   """
#=======================================================



"""
优化算法后的电路为create_qaoa_circ

"""
def create_qaoa_circ(theta):
    nqubits = 4
    p = len(theta) // 2  # number of alternating unitaries
    qc = QuantumCircuit(nqubits)
    beta = theta[:p]
    gamma = theta[p:]
    # initial_state
    for i in range(0, nqubits):
        qc.h(i)
    for irep in range(0, p):
        # problem unitary
        for pair in list(edges):
            if irep == 0:
                if pair == [3, 0]:
                    qc.cx(pair[0], pair[1])
            else:
                qc.cx(pair[0], pair[1])
            qc.rz(2 * gamma[irep], qubit=pair[1])
            qc.cx(pair[0], pair[1])
        # mixer unitary
        for i in range(0, nqubits):
            qc.rx(2 * beta[irep], i)
    qc.measure_all()
    return qc

def get_expectation(p, shots=512):
    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots
    def execute_circ(theta):
        qc = create_qaoa_circ(theta)
        counts = backend.run(qc, seed_simulator=10,
                             nshots=512).result().get_counts()
        return compute_expectation(counts)
    return execute_circ



from scipy.optimize import minimize
expectation = get_expectation(p=1)
print(expectation)


res = minimize(expectation,
                      [1.0, 1.0, 1.0, 1.0],
                      method='COBYLA')
                      # method='BFGS')



from qiskit.visualization import plot_histogram
backend = Aer.get_backend('qasm_simulator')
backend.shots = 512
time_start = time.time()
qc_res = create_qaoa_circ(res.x)
time_end = time.time()
print(time_end - time_start)
print(qc_res)
counts = backend.run(qc_res, seed_simulator=10).result().get_counts()

a = 0
print(counts)
for i in counts:
    a = counts[i] + a
print(a)
# print(counts.keys())
plot_histogram(counts)
plt.show()