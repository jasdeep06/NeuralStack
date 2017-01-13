import numpy as np
import copy
Value={}
strength={}
u_weights = np.array([0,0,0,1,0.5,1])   #pop
d_weights = np.array([1.0,1.0,1,0,0,0]) #push
input_size = 2

initial_temp_strength={}
final_temp_strength={}

initial_strength={}


Value_delta={}
strength_delta={}
push_certainity_delta={}
pop_certainity_delta={}




def read_time(time):
    read=1
    read_vector=np.zeros(input_size)

    temp_strength=copy.deepcopy(strength)
    initial_temp_strength[time]=copy.deepcopy(strength)

    for var in reversed(range(time+1)):
        if temp_strength[var]<read:
            read-=temp_strength[var]
        else:
            temp_strength[var]=read
            unwanted=set(temp_strength.keys())-set(range(var,time+1))

            for keys in unwanted:
                temp_strength[keys]=0
            break
    final_temp_strength[time]=copy.deepcopy(temp_strength)

    for var in Value.keys():
        read_vector+=(temp_strength[var]*Value[var])

    return read_vector


#backpropagation through the read mechanism
def read_time_error(time,r_error):
    temp_strength_error={}
    cache_read=1
    for var in range(time+1):

        temp_strength_error[var]=np.dot(Value[var],r_error.T)
        Value_delta[var]=np.multiply(final_temp_strength[time][var],r_error)
    for var in reversed(range(time+1)):
        if initial_temp_strength[time][var]<cache_read:
            cache_read-=initial_temp_strength[time][var]
            temp_strength_error[var]=-temp_strength_error[var]
        else:
            break
    for var in range(time+1):
        strength_delta[var]=temp_strength_error[var]






def strength_time(time,push_certainity,pop_certainity):
    initial_strength[time] = copy.deepcopy(strength)
    for var in reversed(range(time)):
        if strength[var]<pop_certainity:

            pop_certainity-=strength[var]
            strength[var] = 0
        else:
            strength[var]-=pop_certainity
            pop_certainity = 0
            break

    strength[time] = push_certainity

#backpropogation through strength
def strength_time_error(time,error,push_certainity,pop_certainity):


    push_certainity_delta[time]=error[time]

    for var in reversed(range(time)):
        if initial_strength[time][var]<pop_certainity:


            pop_certainity-=initial_strength[time][var]
            initial_strength[time][var]=0
            pop_certainity_delta[time]+=error[var]
            strength_delta[var]-=error[var]
        else:
            pop_certainity_delta[time]-=error[var]
            strength_delta[var]+=error[var]
            break










def pushPop(push_value,push_certainity,pop_certainity,time,backprop=False,error=None):
    if not backprop:
        strength_time(time,push_certainity,pop_certainity)
        Value[time]=push_value
        return read_time(time)
    else:
        read_time_error(time,error)
        strength_time_error(time,strength_delta,push_certainity,pop_certainity)


for i in range(500):
    if i==0:
        print(u_weights[3])
        print(u_weights[4])
        print(u_weights[5])

    alpha = 5 * ((1 - (float(i) / 500)) ** 2)

    sequence = np.array([[1, 2, 5], [0, 0, 0]]).T

    # RE-INITIALIZE WEIGHTS (empty the stack and strengths)
    Value = {}  # stack states
    strength = {}  # stack strengths
    d = list()  # push strengths
    u = list()  # pop strengths

    Value_delta = {} # stack states
    strength_delta = {}  # stack strengths
    push_certainity_delta = {}
    pop_certainity_delta = {}

    for k in range(6):
        pop_certainity_delta[k] = 0
        push_certainity_delta[k] = 0

    out_0 = pushPop(sequence[0], d_weights[0], u_weights[0], time=0)
    out_1 = pushPop(sequence[1], d_weights[1], u_weights[1], time=1)
    out_2 = pushPop(sequence[2], d_weights[2], u_weights[2], time=2)

    y = np.array([1, 0])

    out_3 = pushPop(sequence[2], d_weights[3], u_weights[3], time=3)
    out_4 = pushPop(sequence[2], d_weights[4], u_weights[4], time=4)
    out_5 = pushPop(sequence[2], d_weights[5], u_weights[5], time=5)




    pushPop(sequence[2], 0, u_weights[5], time=5, backprop=True, error=out_5 - (y * 0.1))
    pushPop(sequence[2], 0, u_weights[4], time=4, backprop=True, error=out_4 - (y * 0.2))
    pushPop(sequence[2], 0, u_weights[3], time=3, backprop=True, error=out_3 - (y * 0.3))


    u_weights[3] -= alpha * pop_certainity_delta[3]
    u_weights[4] -= alpha * pop_certainity_delta[4]
    u_weights[5] -= alpha * pop_certainity_delta[5]

    if (i % 100 == 0):
        print("\n\nIteration:")
        print(i)
        print(out_3[0])
        print(out_4[0])
        print(out_5[0])
        print("u starts")
        print(u_weights[3])
        print(u_weights[4])
        print(u_weights[5])

