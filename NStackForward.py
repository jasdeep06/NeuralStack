import numpy as np
import copy
Value={}
strength={}
input_size=2

value_1=np.zeros(input_size)
value_1[0]=1
value_2=np.zeros(input_size)
value_2[1]=1


def read_time(time):
    #returns read vector at time 'time'

    #initial read value of 1
    read=1
    read_vector=np.zeros(input_size)
    #duplicate of strenth vector to modify it at time of read operation
    temp_strength=copy.deepcopy(strength)
    #traversing through strength vector from top
    for var in reversed(range(time+1)):
        if temp_strength[var]<read:
            read-=temp_strength[var]
        else:
            temp_strength[var]=read

            unwanted=set(temp_strength.keys())-set(range(var,time+1))

            for keys in unwanted:
                temp_strength[keys]=0
            break

    for var in Value.keys():
        read_vector+=(temp_strength[var]*Value[var])

    return read_vector



def strength_time(time,push_certainity,pop_certainity):

    for var in reversed(range(time)):
        if strength[var]<pop_certainity:

            pop_certainity-=strength[var]
            strength[var] = 0
        else:
            strength[var]-=pop_certainity
            pop_certainity = 0
            break

    strength[time] = push_certainity


def pushPop(push_value,push_certainity,pop_certainity,time):

    strength_time(time,push_certainity,pop_certainity)
    Value[time]=push_value
    return read_time(time)

print(pushPop(value_1,1,0.1,0))
print(pushPop(value_2,1,0.5,1))