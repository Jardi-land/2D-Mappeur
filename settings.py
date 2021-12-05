#Variable de base pour la definition de l'ecran
screen_res_array = {1:[1920, 1080],2:[1536, 864],3:[1152, 648],4:[768, 432],5:[384, 216]}
screen_res_numb = 1 # 4 or lower !! not 5 !!
screen_res = screen_res_array[screen_res_numb]
screen_scale = screen_res[0]/1920


window_name = "Mappeur"