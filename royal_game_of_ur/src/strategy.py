import rgu
import numpy as np

num_boards = 16
num_tournaments = 2
alpha = 0.1
mut_prob = 0.7


def mutate(v):
    v_ = v.copy()
    for i, row in enumerate(v_):
        for j, col in enumerate(row):
            if np.random.rand() > mut_prob:
                if np.random.rand() > 0.5:
                    v_[i, j] = max(v_[i, j] - alpha, 0)
                else:
                    v_[i, j] = min(v_[i, j] + alpha, 1)
    return v_


def update_values(v):
    length = len(v)
    num_copies = int((num_boards - length) / length)
    for b in v:
        for i in range(num_copies):
            # print(len(mutate(b)), len(b))

            v = np.append(v, [mutate(b)], axis=0)

    # print(len(v))
    np.random.shuffle(v)
    return v


def init_values():
    return np.random.rand(num_boards, 3, 8)


values = init_values()
game = rgu.RGU()

for epoch in range(1000):
    if epoch % 10 == 0:
        print(epoch)
    winners = list(range(num_boards))
    values = update_values(values)

    while len(winners) > 2:
        temp = []

        for i in range(0, len(winners), 2):
            game.new_game()
            game.board_values = values[i: i + 2]
            temp.append(game.play_automated() + i)

        winners = temp
        values = values[winners]

print(values)

"""
[[[ 2.12899862 -1.94372679  4.61896157 -0.71309179  2.9088326   2.88175053
   -0.59207986  1.10690222]
  [ 2.48175842  0.56767907 -0.09414909  1.71107248 -0.71730299  2.24665514
    0.88095251 -1.01279484]
  [ 0.77165301 -0.70838524  1.18265237  1.7804434  -0.94315697 -0.16866618
   -0.33109534 -1.6874568 ]]

 [[ 2.02899862 -1.84372679  4.81896157 -0.81309179  3.1088326   2.68175053
   -0.69207986  1.10690222]
  [ 2.58175842  0.56767907 -0.09414909  1.71107248 -0.71730299  2.14665514
    0.98095251 -1.01279484]
  [ 0.57165301 -0.80838524  1.08265237  1.7804434  -0.94315697 -0.06866618
   -0.43109534 -1.6874568 ]]]

   [[[ 0.9  0.6  0.4  0.8  0.1  1.   0.7  0.8]
  [ 0.2  0.7  0.   1.   1.   0.6  0.2  0.7]
  [ 0.2  0.5  0.9  0.9  0.   0.3  0.4  0.5]]

 [[ 0.9  0.6  0.5  0.8  0.2  0.9  0.7  0.8]
  [ 0.2  0.7  0.   1.   1.   0.6  0.2  0.7]
  [ 0.2  0.3  0.8  0.8  0.   0.2  0.4  0.4]]]
"""
