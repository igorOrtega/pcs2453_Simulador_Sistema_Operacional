from processor import Processor

a = Processor(5)
print(a.request(1,1))
print(a.roundRobin.avaiablePositions)
print(a.release(1))
print(a.roundRobin.avaiablePositions)
