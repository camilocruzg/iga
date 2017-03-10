__author__ = 'ccruz'
from numpy import asarray, save
from functions import init_state

size = (50,50)

init_states_X = []
init_states_Y = []

for i in range(1):
    isX = init_state(size, 'x', 'random',0.5)
    isY = init_state(size, 'y', 'random',0.5)
    init_states_X.append(isX)
    init_states_Y.append(isY)

init_states_X = asarray(init_states_X)
init_states_Y = asarray(init_states_Y)

init_states_X_10 = init_states_X[:,:11,:11]
init_states_Y_10 = init_states_Y[:,:11,:11]

print init_states_X_10

init_states_X_20 = init_states_X[:,:21,:21]
init_states_Y_20 = init_states_Y[:,:21,:21]

init_states_X_50 = init_states_X[:,:51,:51]
init_states_Y_50 = init_states_Y[:,:51,:51]

save('init_states_X_10',init_states_X_10)
save('init_states_Y_10', init_states_Y_10)

save('init_states_X_20',init_states_X_20)
save('init_states_Y_20', init_states_Y_20)

save('init_states_X_50',init_states_X_50)
save('init_states_Y_50', init_states_Y_50)