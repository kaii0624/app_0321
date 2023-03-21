import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import os


#draw_2Dのパラメータ設定
color_matrix = {0:"white",5:"yellow",2:"green",3:"red",4:"blue",1:"orange",6:"gray",7:"pink",8:"black"}
face_colors = {"U":0,"L":1,"F":2,"R":3,"B":4,"D":5}

d_center =3
width_center = 2.95
width_piece = 1.2
x_screen_offset =0.2
y_screen_offset =0.2


d_screen = 2 * d_center + width_center + 2 * y_screen_offset
width_screen =  3*  d_center + width_center + 2 * x_screen_offset
x_0 = d_center + width_center/2 + y_screen_offset
y_0 = d_center + width_center/2 + y_screen_offset

#draw_2Dの関数設定

def rec(x,y,w,h,c):
    rec = pat.Rectangle(xy = (x - w/2,  y - h/2) , width = w, height = h, color = color_matrix[c])
    ax.add_patch(rec)

def draw_frame(List):
    center_position = {"U":(x_0 , y_0 + d_center),"L":(x_0 - d_center , y_0),"F":(x_0 , y_0),
    "R":(x_0 + d_center , y_0),"B":(x_0 + 2 * d_center , y_0),"D":(x_0 , y_0 - d_center)}
    for i in "ULFRBD":
        x, y = center_position[i]
        rec(x,y, width_center, width_center, 8)

def apply_color(List):
    d_piece = 1.5
    cp= List[0:8]
    co= List[8:16]
    c0=[0,0,0,0,0,0,0,0]
    c1=[0,0,0,0,0,0,0,0]
    c2=[0,0,0,0,0,0,0,0]
    
    color_C = [0,0,0,0,5,5,5,5]
    color_cw = [1,4,3,2,4,3,2,1]
    color_ccw = [4,3,2,1,1,4,3,2]
    position_C = [(3,6.2+d_piece),(3+d_piece,6.2+d_piece),(3+d_piece,6.2),(3,6.2),(3,0.2),(3+d_piece,0.2),(3+d_piece,0.2+d_piece),(3,0.2+d_piece)]
    position_cw = [(0,3.2+d_piece),(9,3.2+d_piece),(6,3.2+d_piece),(3,3.2+d_piece),(9+d_piece,3.2),(6+d_piece,3.2),(3+d_piece,3.2),(d_piece,3.2)]
    position_ccw = [(9+d_piece,3.2+d_piece),(6+d_piece,3.2+d_piece),(3+d_piece,3.2+d_piece),(d_piece,3.2+d_piece),(0,3.2),(9,3.2),(6,3.2),(3,3.2)]

    for n in range(8):
        if co[n]==0: #UD面に,パーツ0がある状態
            c0[n] = color_C[cp[n]]
            c1[n] = color_ccw[cp[n]]
            c2[n] = color_cw[cp[n]]

        if co[n] == 1:
            c0[n] = color_ccw[cp[n]]
            c1[n] = color_cw[cp[n]]
            c2[n] = color_C[cp[n]]

        if co[n] == 2:
            c0[n] = color_cw[cp[n]]
            c1[n] = color_C[cp[n]]
            c2[n] = color_ccw[cp[n]]

        x0,y0 = position_C[n]
        x1,y1 = position_ccw[n]
        x2,y2= position_cw[n]
        
        xf, yf = 0.3,0.105

        r0 = pat.Rectangle(xy = (x0+ xf,y0+ yf), width = width_piece, height = width_piece, color =  color_matrix[c0[n]])
        r1 = pat.Rectangle(xy = (x1+ xf,y1+ yf), width = width_piece, height = width_piece, color =  color_matrix[c1[n]])
        r2 = pat.Rectangle(xy = (x2+ xf,y2+ yf), width = width_piece, height = width_piece, color =  color_matrix[c2[n]])
        ax.add_patch(r0)
        ax.add_patch(r1)
        ax.add_patch(r2)

def draw_2d_cube(List):
    global fig 
    global ax
    fig = plt.figure(figsize=(8.5, 8.5))
    ax = fig.add_subplot(111)
    
    ax.set_xlim(0, width_screen)
    ax.set_ylim(0, d_screen)
    ax.set_aspect('equal')
    plt.tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False)
    plt.tick_params(bottom=False,left=False,right=False,top=False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    draw_frame(List)
    apply_color(List)


    figname =  "now_cube2D.png"
    plt.close(fig)
    #現在のパスに保存
    fig.savefig("" + figname, transparent=True)
    return fig

#cube rotation definition
class State:
    def __init__(self, cp, co):
        self.cp = np.array(cp, dtype='int8')
        self.co = np.array(co, dtype='int8')

    def apply_move(self, move):
        new_cp = self.cp[move.cp]
        new_co = (self.co[move.cp] + move.co) % 3
        return State(new_cp, new_co)

def rotation_cube(str_state, move):
    global_scramble_state = str_to_state(str_state).apply_move(moves[move])
    return state_to_str(global_scramble_state)

def list_to_state(List):
    return State(List[0:8], List[8:16])
    
def state_to_list(state):
    return list(state.cp)+list(state.co)

def str_to_state(s):
    corner_values = [int(c) for c in s[:8]]
    edge_values = [int(e) for e in s[8:]]
    return State(corner_values, edge_values)

def list_to_str(lst):
    return ''.join(str(e) for e in lst)

def state_to_str(state):
    lst = state_to_list(state)
    return list_to_str(lst)

def str_to_list(s):
    return [int(c) for c in s]



#キューブのパラメータを定義する
global_scramble_state = State([0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0])

moves = {
    'U': State([3, 0, 1, 2, 4, 5, 6, 7],[0, 0, 0, 0, 0, 0, 0, 0]),
    'D': State([0, 1, 2, 3, 5, 6, 7, 4],[0, 0, 0, 0, 0, 0, 0, 0]),
    'L': State([4, 1, 2, 0, 7, 5, 6, 3],[2, 0, 0, 1, 1, 0, 0, 2]),
    'R': State([0, 2, 6, 3, 4, 1, 5, 7],[0, 1, 2, 0, 0, 2, 1, 0]),
    'F': State([0, 1, 3, 7, 4, 5, 2, 6],[0, 0, 1, 2, 0, 0, 2, 1]),
    'B': State([1, 5, 2, 3, 0, 4, 6, 7],[1, 2, 0, 0, 2, 1, 0, 0])
}

move_names = []
for face_name in list(moves.keys()):
    move_names += [face_name, face_name + '2', face_name + '\'']
    moves[face_name + '2'] = moves[face_name].apply_move(moves[face_name])
    moves[face_name + '\''] = moves[face_name].apply_move(moves[face_name]).apply_move(moves[face_name])
    
    
CSV_FILE = 'moves.csv'


def cube(state):
    return f'{int(state) + 1:05d}'

def update_csv(move, state):
    with open(CSV_FILE, 'a') as f:
        f.write(f'"{move}","{state}"\n')  # Add double quotes around move and state

def read_last_state():
    df = pd.read_csv(CSV_FILE, dtype=str)  # Force all columns to be read as strings
    last_state = df.iloc[-1]['state']
    return last_state

def main():
    st.title('Streamlit Cube App')
    solved_placeholder = st.empty()

    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write('"moves","state"\n')
            f.write('"Initial","0123456700000000"\n')

    button_labels = [
        'R', 'U', 'D', 'L', 'B', 'F',
        "R'", "U'", "D'", "L'", "B'", "F'"
    ]

    # 最初に画像を表示
    initial_str_state = read_last_state()
    draw_2d_cube(str_to_list(initial_str_state))
    image_placeholder = st.empty()
    image_placeholder.image('now_cube2D.png')

    for button_label in button_labels:
        if st.button(button_label):
            move = button_label
            current_str_state = read_last_state()
            new_state = rotation_cube(current_str_state, move)
            update_csv(move, new_state)
            draw_2d_cube(str_to_list(new_state))
            image_placeholder.image('now_cube2D.png')

            if new_state == "0123456700000000":
                solved_placeholder.markdown("<h1 style='text-align: left; color: red;'>Solved!</h1>", unsafe_allow_html=True)
            else:
                solved_placeholder.empty()

    if st.button("reset"):
        with open(CSV_FILE, 'w') as f:
            f.write('"moves","state"\n')
            f.write('"Initial","0123456700000000"\n')
        draw_2d_cube(str_to_list(read_last_state()))
        image_placeholder.image('now_cube2D.png')

if __name__ == '__main__':
    main()
