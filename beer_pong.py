import numpy as np
import random

class drinks:
    "This class is used to define attributes for the type of drinks players are drinking and their alcohol content."
    def __init__(self,drink_type):
        '''Initialize the drink type and contains alcohol attributes'''
        self.drink_type = drink_type  #set the drink_type attribute
        if self.drink_type.lower() not in ['wine','beer','water','liquor']:
            raise Exception ('Please enter a following drink: wine, beer, liquor, or water')  #if user doesn't input a valid drink raise exception
        if self.drink_type.lower() == 'water':   #set the contains_alcohol attribute to determine if a players BAC will increase if the other team hits a cup
            self.contains_alcohol = False
        else:
            self.contains_alcohol = True

class balls:
    '''This class defines key attributes of the ball including it’s diameter and if it’s dented.'''
    def __init__(self):
        '''Initialize the diameter and dented attributes of the ball'''
        self.diameter = 40 #diameter in milimeters
        self.dented = False #if the ball is dented, begins not dented

class cups:
    #Make this inherit from teams class
    """The cups class is used to define and update the order of each team's cups throughout the game"""
    def __init__(self):
        '''Initialize the order of the cups and the rack names and cup count, etc.'''
        self.start_order = [[1],[2,3],[4,5,6],[7,8,9,10]]  #nested list shows levels of current cup order and numbers in the order refer to the cup position
        self.current_order = self.start_order  #each game will start with the cups in the starting order
        self.current_rack = 'starting rack'   #naming the rack will be important for reracks and printing the cups in the correct order
        self.total_cups = [1,2,3,4,5,6,7,8,9,10]  #total cups keeps track of all available cup positions, if a cup is hit the position number turns to 0 / null
        self.cup_count = 10 #counts total cups remaining for a team
        self.total_throws = 0 #counts total throws for a given team / set of cups
        self.reracks_remaining = 2 #sets each set of team's cups reracks to two

    def adjacent(self, aiming_cup_position):
        '''This function determines a list of cups adjacent to the cup that is being aimed at and counts the number of adjacent cups.
         This will be helpful when determining the probability a player shoots a ball into a cup adjacent to what they were aiming at.'''
        self.aiming_cup_position = aiming_cup_position

        #define all adjacent cups for each cup position in dictionaries based on each possible rack order
        adjacent_cups_dict_starting_rack = {1: [2,3], 2 : [1,3,4,5], 3 : [1,2,5,6], 4 : [2,5,7,8], 5 : [2,3,4,6,8,9], 6 : [3,5,9,10], 7 : [4,8], 8 : [4,5,7,9], 9 : [5,6,8,10], 10 : [6,9]}
        adjacent_cups_dict_gentlemans = {1 : [11], 11 : [1]}
        adjacent_cups_dict_stoplight = {1 : [11], 11 : [1,12], 12 : [11]}
        adjacent_cups_dict_three_triangle = {1 : [2,3], 2 : [1,3], 3 : [1,2]}
        adjacent_cups_dict_diamond = {1: [2,3], 2 : [1,3,5], 3 : [1,2,5], 5 : [2,3]}
        adjacent_cups_dict_zipper = {1 : [11, 13], 11 : [12, 13, 14], 12 : [11, 14], 13 : [1, 11, 14], 14 : [11, 12, 13]}
        adjacent_cups_dict_six_triangle = {1: [2,3], 2 : [1,3,4,5], 3 : [1,2,5,6], 4 : [2,5], 5 : [2,3,4,6], 6 : [3,5]}

        if self.aiming_cup_position not in self.total_cups:  #stop users who aim at cups that no longer exist in the game
            raise Exception ('Please aim at a cup position that is still in the game')
        else:
            #assign the adjacent_list of adjacent cups given a current rack order and the aiming cup postion
            #count the number of adjacent cups given a current rack order and the aiming cup position. The more adjacent cups, the more likely a user will hit an adjacent cup.
            if self.current_rack == 'starting rack':
                self.adjacent_list = adjacent_cups_dict_starting_rack[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == 'gentleman\'s':
                self.adjacent_list = adjacent_cups_dict_gentlemans[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == '3 triangle':
                self.adjacent_list =  adjacent_cups_dict_three_triangle[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == 'stoplight':
                self.adjacent_list =  adjacent_cups_dict_stoplight[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == 'diamond':
                self.adjacent_list =  adjacent_cups_dict_diamond[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == 'zipper':
                self.adjacent_list =  adjacent_cups_dict_zipper[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)
            if self.current_rack == '6 triangle':
                self.adjacent_list =  adjacent_cups_dict_six_triangle[self.aiming_cup_position]
                self.total_adjacent = len(self.adjacent_list)

    def rerack(self, rerack_type):
        """This function reracks the cups to update their current position. A rerack can occur only at the beginnning of the team requesting the rerack's turn. """
        self.rerack_type_list = ['gentleman\'s', '3 triangle','stoplight','diamond','zipper','6 triangle']

        #raise exception if user has already used all reracks
        if self.reracks_remaining <= 0:
            raise Exception('You do not have any more reracks remaining')

        #raise exception if user doesn't enter a valid rerack type
        if rerack_type.lower() not in self.rerack_type_list:
            raise Exception('Please enter a valid rerack type: gentleman\'s, 3 triangle, stoplight, diamond, zipper, 6 triangle')
        else:
            self.rerack_type = rerack_type.lower()

        #raise an Exception if the user selected a rerack type with an incorrect number of cups for the rerack
        #Update the current order, total cups, and current rack values given the rerack information
        if self.rerack_type == 'gentleman\'s':
            if self.cup_count != 2:
                raise Exception ('You can only do a gentleman\'s rerack with 2 cups')
            else:
                self.current_order = [[1],[11]]
                self.total_cups = [1,11]
                self.current_rack = 'gentleman\'s'

        elif self.rerack_type == '3 triangle':
            if self.cup_count != 3:
                raise Exception ('You can only do a 3 triangle rerack with 3 cups')
            else:
                self.current_order = [[1],[2,3]]
                self.total_cups = [1,2,3]
                self.current_rack = '3 triangle'

        elif self.rerack_type == 'stoplight':
            if self.cup_count != 3:
                raise Exception ('You can only do a stoplight rerack with 3 cups')
            else:
                self.current_order = [[1],[11],[12]]
                self.total_cups = [1,11,12]
                self.current_rack = 'stoplight'

        elif self.rerack_type == 'diamond':
            if self.cup_count != 4:
                raise Exception ('You can only do a diamond rerack with 4 cups')
            else:
                self.current_order = [[1],[2,3],[5]]
                self.total_cups = [1,2,3,5]
                self.current_rack = 'diamond'

        elif self.rerack_type == 'zipper':
            if self.cup_count != 5:
                raise Exception ('You can only do a zipper rerack with 5 cups')
            else:
                self.current_order = [[1],[13],[11],[14],[12]]
                self.total_cups = [1,13,11,14,12]
                self.current_rack = 'zipper'

        elif self.rerack_type == '6 triangle':
            if self.cup_count != 6:
                raise Exception ('You can only do a 6 triangle rerack with 6 cups')
            else:
                self.current_order = [[1],[2,3],[4,5,6]]
                self.total_cups = [1,2,3,4,5,6]
                self.current_rack = '6 triangle'
        self.reracks_remaining -= 1

    def __str__(self):
        """Prints the current cup arrangement for each team"""
        #see attached document for the expected outputs for each rerack type, and each cup position number
        print_str = ''

        if self.current_rack == 'starting rack':
            for i in range(0, len(self.current_order)):
                print_str += ' ' * (3 - i)
                for j in range(0, i+1):
                    if self.current_order[i][j] == 0:
                        print_str += '   '
                    else:
                        print_str += '( )'
                print_str += '\n'
            return print_str

        elif self.current_rack == 'gentleman\'s':
            for i in self.total_cups:
                if i != 0: #account for cups that have been hit and have an updated position value of 0
                    print_str += '( )'
                else:
                    print_str += ''
                print_str += '\n'
            return print_str

        elif self.current_rack == '3 triangle':
            for i in range(0,len(self.current_order)):
                print_str += (' '* (1 - i))
                for j in range(0,i+1):   #print a space if there is no cup in that position
                    if self.current_order[i][j] == 0:
                        print_str += '   '
                    else:
                        print_str += '( )'
                print_str += '\n'
            return print_str

        elif self.current_rack == 'stoplight':
            for i in self.total_cups:
                if i != 0:
                    print_str += '( )'
                else:
                    print_str += ''
                print_str += '\n'
            return print_str

        elif self.current_rack == 'diamond':
            print_str += ' '
            for i in range(0, len(self.current_order)):
                if i == 2:
                    print_str += ' '
                    if self.current_order[i][0] == 0:
                        print_str += ''
                    else:
                        print_str += '( )'
                else:
                    for j in range(0,len(self.current_order[i])):
                        if self.current_order[i][j] == 0:
                            print_str += '   '
                        else:
                            print_str += '( )'
                    print_str += '\n'
            return print_str

        elif self.current_rack == 'zipper':
            for i in range(0,len(self.total_cups)):
                if i%2 != 0:
                    if self.total_cups[i] == 0:
                        print_str += ''
                    else:
                        print_str += '( )'
                else:
                    if self.total_cups[i] == 0:
                        print_str += ''
                    else:
                        print_str += ' ( )'
                print_str += '\n'
            return print_str

        elif self.current_rack == '6 triangle':
            for i in range(0,len(self.current_order)):
                print_str += (' '* (2 - i))
                for j in range(0,i+1):   #print a space if there is no cup in that position
                    if self.current_order[i][j] == 0:
                        print_str += '   '
                    else:
                        print_str += '( )'
                print_str += '\n'
            return print_str

class players:  #add exceptions for all inputs to direct user
    '''The player class defines key details of each player that help keep track of who is shooting, and their accuracy'''
    def __init__(self,player_name,player_number,player_team_number,player_gender,player_weight,player_skill_level):
        '''Initialize the players name, number, team number, gender, weight, skill level, BAC, and drink count attributes'''
        self.player_name = player_name
        self.player_number = player_number
        self.player_team_number = player_team_number
        self.player_gender = player_gender
        self.player_weight = player_weight
        self.player_skill_level = player_skill_level #player skill level is on a scale from one to ten (one: beginner, five: average, ten: expert)
        self.player_BAC = 0
        self.drink_count = 0 #drink count only counts alcoholic beverages consumed

    def BAC(self):
        '''BAC function is based on tables found at https://www.iup.edu/WorkArea/DownloadAsset.aspx?id=128966
        the timespan of drinking is one hour, assuming the game is played at a normal speed, and the drinks are assumed to all be one standard size drink, regardless of the type of alcohol'''
        BAC_females ={100 : [0.04, 0.09, 0.14, 0.19, 0.24, 0.29, 0.34, 0.39, 0.45, 0.50], 110 : [0.03, 0.08, 0.13, 0.17, 0.22, 0.27, 0.31, 0.36, 0.40, 0.45], 120 : [0.03, 0.07, 0.12, 0.16, 0.20, 0.24, 0.28, 0.33, 0.37, 0.41], 130 : [0.03, 0.07, 0.11, 0.14, 0.18, 0.22, 0.26, 0.30, 0.34, 0.38], 140 : [0.02, 0.06, 0.10, 0.13, 0.17, 0.21, 0.24, 0.28, 0.31, 0.35], 150 : [0.02, 0.06, 0.09, 0.12, 0.16, 0.19, 0.23, 0.26, 0.29, 0.33], 160 : [0.02, 0.05, 0.08, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.31], 170 : [0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.20, 0.23, 0.26, 0.29], 180 : [0.02, 0.04, 0.07, 0.10, 0.13, 0.16, 0.19, 0.21, 0.24, 0.27], 190 : [0.01, 0.04, 0.07, 0.10, 0.12, 0.15, 0.18, 0.20, 0.23, 0.26], 200 : [0.01, 0.04, 0.06, 0.09, 0.12, 0.14, 0.17, 0.19, 0.22, 0.24], 210 : [0.01, 0.04, 0.06, 0.08, 0.11, 0.13, 0.16, 0.18, 0.21, 0.23], 220 : [0.01, 0.03, 0.06, 0.08, 0.10, 0.13, 0.15, 0.17, 0.20, 0.22], 230 : [0.01, 0.03, 0.05, 0.08, 0.10, 0.12, 0.14, 0.16, 0.19, 0.21], 240 : [0.01, 0.03, 0.05, 0.07, 0.09, 0.12, 0.14, 0.16, 0.18, 0.20]}
        BAC_males = {110 : [0.03, 0.07, 0.11, 0.14, 0.18, 0.22, 0.26, 0.30, 0.34, 0.38], 120 : [0.02, 0.06, 0.10, 0.13, 0.17, 0.20, 0.24, 0.27, 0.31, 0.35], 130 : [0.02, 0.05, 0.09, 0.12, 0.15, 0.19, 0.22, 0.25, 0.29, 0.32], 140 : [0.02, 0.05, 0.08, 0.11, 0.14, 0.17, 0.20, 0.23, 0.26, 0.29], 150 : [0.02, 0.05, 0.07, 0.10, 0.13, 0.16, 0.19, 0.22, 0.25, 0.27], 160 : [0.01, 0.04, 0.07, 0.10, 0.12, 0.15, 0.18, 0.20, 0.23, 0.26], 170 : [0.01, 0.04, 0.06, 0.09, 0.11, 0.14, 0.16, 0.19, 0.22, 0.24], 180 : [0.01, 0.04, 0.06, 0.08, 0.11, 0.13, 0.15, 0.18, 0.20, 0.23], 190 : [0.01, 0.03, 0.06, 0.08, 0.10, 0.12, 0.15, 0.17, 0.19, 0.21], 200 : [0.01, 0.03, 0.05, 0.07, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20], 210 : [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19], 220 : [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.12, 0.14, 0.16, 0.18], 230 : [0.01, 0.03, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.17], 240 : [0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.11, 0.13, 0.15, 0.17], 250 : [0.01, 0.02, 0.04, 0.06, 0.07, 0.09, 0.11, 0.13, 0.14, 0.16]}

        if self.player_gender == 'female':
            self.player_BAC = BAC_females[self.player_weight][self.drink_count]
        if self.player_gender == 'male':
            self.player_BAC = BAC_males[self.player_weight][self.drink_count]

    def shooting_accuracy(self):
        '''This function determines the shooting accuracy for each player depending on their BAC and skill level. As the number of drinks a player takes increases, so will their BAC, and therefore, their shoot accuracy will decrease.'''
        self.accuracy = self.player_skill_level *(-5 * self.player_BAC + 1.5) #used linear scale to make .1 BAC not affect accuracy (coefficient of 1) and BAC of .3 to make the coefficient 0
        if self.accuracy <= 1:
            self.accuracy = 1  #gives player lowest possible accuracy level, so nobody is shooting with 0 accuracy or 0.1 accuracy, etc.
class teams:
    def __init__(self, team_number, player_list, starting):
        '''This class defines which players are part of which team, who starts, and how many reracks are remaining.'''
        self.team_number = team_number
        self.player_list = player_list
        self.starting = starting #0 / 1 value to determine if the team is starting
        #self.reracks_remaining = 2

def take_drink(drink, player):
    """This function simulates a player taking an alcoholic drink, which increases their total drink count and calls the BAC function to update the player's BAC"""
    if drink.contains_alcohol == True:
        player.drink_count += 1
        player.BAC()

def dent_ball(ball, cup_set_a, cup_set_b):
    '''This function is ran after a ball is thrown and will use a probability function to determine if the ball becomes dented, affecting the probability the ball will land in a cup.'''
    if ball.dented:
        return
    else:
        mu = .5 + (cup_set_a.total_throws * .0025) #adjust average to be closer to one as throws increase
        probability_of_dent = np.random.normal(mu, 0.1, 1) #output is a one value array
        if probability_of_dent[0] >= 1:
            ball.dented = True
            print("Oh no, your ball is now dented.")
        else:
            ball.dented = False

def throw_ball(ball, cup, team, player, aiming_cup_position):
    '''This function simulates a player throwing a ball and will output if the ball landed in the cup or not by updating the current order of the cups'''
    cup.adjacent(aiming_cup_position)#return count and list of adjacent cups to the cup player is aiming at
    player.shooting_accuracy()
    if ball.dented == False:
        mu_aiming =  player.accuracy / 10
        mu_adjacent = mu_aiming * (cup.total_adjacent * .256 + 0.64) #change in factors is based on 'gut feeling' of how your chance would be half as high to hit an adjacent cup vs the cup you were aiming at if only 2 cups were present and 60% higher if you had 6 adjacent cups
        aiming_cup_probability = np.random.normal(mu_aiming, 0.25, 1)
        adjacent_cup_probability = np.random.normal(mu_adjacent,0.25,1)
        if aiming_cup_probability >= 1: #player hits cup they're aiming at
            cup_out = aiming_cup_position
            index_1 = find_in_list_of_list(cup.current_order, cup_out)
            cup.current_order[index_1[0]][index_1[1]] = 0
            index = cup.total_cups.index(cup_out)
            cup.total_cups[index] = 0
            cup.cup_count -= 1
            print(f"Congratulations, you hit the cup you were aiming at in position {aiming_cup_position}")
        elif adjacent_cup_probability >= 1 and len(cup.adjacent_list) > 0 :
            x = 1
            while x == 1: #ensure no hit cups are part of the adjacent cup list
                cup_out = cup.adjacent_list[random.randrange(0,len(cup.adjacent_list),1)]
                if cup_out in cup.total_cups:
                    x = 0
                else:
                    cup.adjacent_list.remove(cup_out)
            index_1 = find_in_list_of_list(cup.current_order, cup_out)
            cup.current_order[index_1[0]][index_1[1]] = 0
            index = cup.total_cups.index(cup_out)
            cup.total_cups[index] = 0
            cup.cup_count -= 1
            print(f"Congratulations, you hit an adjacent cup in position {cup_out}")
        else:
            print("Too bad! You didn\'t hit a cup.")
    else: #if ball is dented
        #shooting accuracy decreases by 10% if the ball is dented
        mu_aiming =  player.accuracy / 10 * 0.9
        mu_adjacent = mu_aiming * (cup.total_adjacent * .256 + 0.64) #change in factors is based on: if only 2 adjacent cups are present, your chance of hitting an adjacent cup is 50% less than your chance of hitting the cup you're aiming at, and if 6 adjacent cups are present, your chance of hitting an adjacent cup is 60% higher than hitting the cup you're aiming at
        aiming_cup_probability = np.random.normal(mu_aiming, 0.25, 1)
        adjacent_cup_probability = np.random.normal(mu_adjacent,0.25,1)
        if aiming_cup_probability >= 1: #player hits cup they're aiming at
            cup_out = aiming_cup_position
            index_1 = find_in_list_of_list(cup.current_order, cup_out)
            cup.current_order[index_1[0]][index_1[1]] = 0
            index = cup.total_cups.index(cup_out)
            cup.total_cups[index] = 0
            cup.cup_count -= 1
            print(f"Congratulations, you hit the cup you were aiming at in position {aiming_cup_position}")
        elif adjacent_cup_probability >= 1 and len(cup.adjacent_list) > 0 :
            x = 1
            while x == 1: #ensure no hit cups are part of the adjacent cup list
                cup_out = cup.adjacent_list[random.randrange(0,len(cup.adjacent_list),1)]
                if cup_out in cup.total_cups:
                    x = 0
                else:
                    cup.adjacent_list.remove(cup_out)
            index_1 = find_in_list_of_list(cup.current_order, cup_out)
            cup.current_order[index_1[0]][index_1[1]] = 0
            index = cup.total_cups.index(cup_out)
            cup.total_cups[index] = 0
            cup.cup_count -= 1
            print(f"Congratulations, you hit an adjacent cup in position {cup_out}")
        else:
            print("Too bad! You didn\'t hit a cup.")
    cup.total_throws += 1

def find_in_list_of_list(mylist, char):
    '''This function searches for an index of an item in a nested list.'''
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))

#initiate the drink class
drink_type_input = input('Please enter a the type of drink you will be using: ')
alc_type = drinks(drink_type_input)

#initiate the balls class creation
ball = balls()

#initiate team one and twos set of cups
cups_team_1 = cups()
cups_team_2 = cups()

#initiate player 1 on team 1
player_1_name_input = input('Please enter the name of player 1 on team 1: ')
player_1_gender_input = input('Please enter the gender of player 1 on team 1: ')
if player_1_gender_input != 'female' and player_1_gender_input != 'male':
    raise Exception('Please enter either female or male as the gender')
player_1_weight_input = int(input('Please enter the weight of player 1 on team 1: '))
if player_1_gender_input == 'female':
    if player_1_weight_input not in [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240]:
        raise Exception('Female player weights have to be rounded to the nearest ten digits from 100 lbs to 240 lbs')
else:
    if player_1_weight_input not in [110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]:
        raise Exception('Male player weights have to be rounded to the nearest ten digits from 110 lbs to 250 lbs')

player_1_skill_input = int(input('Please enter the skill level of player 1 on team 1: '))
if player_1_skill_input not in [1,2,3,4,5,6,7,8,9,10]:
    raise Exception("Skill level is an integer between one and ten")
player_1_team_1 = players(player_1_name_input,1,1,player_1_gender_input,player_1_weight_input,player_1_skill_input)

#initiate player 2 on team 1
player_2_name_input = input('Please enter the name of player 2 on team 1: ')
player_2_gender_input = input('Please enter the gender of player 2 on team 1: ')
if player_2_gender_input != 'female' and player_2_gender_input != 'male':
    raise Exception('Please enter either female or male as the gender')
player_2_weight_input = int(input('Please enter the weight of player 2 on team 1: '))
if player_2_gender_input == 'female':
    if player_2_weight_input not in [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240]:
        raise Exception('Female player weights have to be rounded to the nearest ten digits from 100 lbs to 240 lbs')
else:
    if player_2_weight_input not in [110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]:
        raise Exception('Male player weights have to be rounded to the nearest ten digits from 110 lbs to 250 lbs')

player_2_skill_input = int(input('Please enter the skill level of player 2 on team 1: '))
if player_2_skill_input not in [1,2,3,4,5,6,7,8,9,10]:
    raise Exception("Skill level is an integer between one and ten")
player_2_team_1 = players(player_2_name_input,2,1,player_2_gender_input,player_2_weight_input,player_2_skill_input)

#initiate player 1 on team 2
player_3_name_input = input('Please enter the name of player 1 on team 2: ')
player_3_gender_input = input('Please enter the gender of player 1 on team 2: ')
if player_3_gender_input != 'female' and player_3_gender_input != 'male':
    raise Exception('Please enter either female or male as the gender')
player_3_weight_input = int(input('Please enter the weight of player 1 on team 2: '))
if player_3_gender_input == 'female':
    if player_3_weight_input not in [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240]:
        raise Exception('Female player weights have to be rounded to the nearest ten digits from 100 lbs to 240 lbs')
else:
    if player_3_weight_input not in [110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]:
        raise Exception('Male player weights have to be rounded to the nearest ten digits from 110 lbs to 250 lbs')

player_3_skill_input = int(input('Please enter the skill level of player 1 on team 2: '))
if player_3_skill_input not in [1,2,3,4,5,6,7,8,9,10]:
    raise Exception("Skill level is an integer between one and ten")
player_1_team_2 = players(player_3_name_input,1,2,player_3_gender_input,player_3_weight_input,player_3_skill_input)

#initiate player 2 on team 2
player_4_name_input = input('Please enter the name of player 2 on team 2: ')
player_4_gender_input = input('Please enter the gender of player 2 on team 2: ')
if player_4_gender_input != 'female' and player_4_gender_input != 'male':
    raise Exception('Please enter either female or male as the gender')
player_4_weight_input = int(input('Please enter the weight of player 2 on team 2: '))
if player_4_gender_input == 'female':
    if player_4_weight_input not in [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240]:
        raise Exception('Female player weights have to be rounded to the nearest ten digits from 100 lbs to 240 lbs')
else:
    if player_4_weight_input not in [110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]:
        raise Exception('Male player weights have to be rounded to the nearest ten digits from 110 lbs to 250 lbs')

player_4_skill_input = int(input('Please enter the skill level of player 2 on team 2: '))
if player_4_skill_input not in [1,2,3,4,5,6,7,8,9,10]:
    raise Exception("Skill level is an integer between one and ten")
player_2_team_2 = players(player_4_name_input,1,2,player_4_gender_input,player_4_weight_input,player_4_skill_input)

#initiate team 1
starting_team = int(input('Please enter the number of which team you would like to start the game: '))#int input
if starting_team == 1:
    team_1 = teams(1,[player_1_team_1,player_2_team_1],1)
elif starting_team == 2:
    team_1 = teams(1,[player_1_team_1,player_2_team_1],0)
else:
    raise Exception("Please enter a valid starting team value.")

#initiate team 2
if starting_team == 2:
    team_2 = teams(1,[player_1_team_2,player_2_team_2],1)
else:
    team_2 = teams(1,[player_1_team_2,player_2_team_2],0)

#--------- Initialization complete -------------
#begin by printing starting rack of cups
print(cups_team_2)

#loop through the game until one team hits all their cups
while cups_team_2.cup_count > 0 and cups_team_1.cup_count > 0:
    #first half of loop if team two is starting
    if team_2.starting == 1:
        #set counter for original number of cups
        start_cup_amount_1 = cups_team_2.cup_count

        #determine if a player can and wants to rerack the cups
        if start_cup_amount_1 <= 6 and start_cup_amount_1 > 1 and cups_team_2.reracks_remaining != 0:
            rerack_desired = input("Would you like to rerack your cups (Y/N)?")
            if rerack_desired == 'Y':
                type_of_rerack = input("What type of rerack would you like? ")
                cups_team_2.rerack(type_of_rerack)
                print("This is your new rack of cups!")
                print(cups_team_2)
            elif rerack_desired == 'N':
                continue
            else:
                raise Exception ('Please enter either Y or N.')

        #determine aiming cup and throw ball
        aiming_cup_1 = int(input("Player 1 of team 2, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_2, team_2, player_1_team_2, aiming_cup_1)

        #make opposing player take a drink if a cup was hit
        if cups_team_2.cup_count != start_cup_amount_1:
            take_drink(alc_type,player_1_team_1)

        #see if ball is dented after that throw and print output of cups
        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_2)

        #repeat the above steps for all other players
        #player 2 on team 2
        start_cup_amount_2 = cups_team_2.cup_count

        aiming_cup_2 = int(input("Player 2 of team 2, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_2, team_2, player_2_team_2, aiming_cup_2)

        if cups_team_2.cup_count != start_cup_amount_2:
            take_drink(alc_type, player_2_team_1)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_2)

        #break out of loop if team 2 won
        if cups_team_2.cup_count == 0:
            break

        #player 1 on team 1
        print('It\'s now team 1\'s turn')
        print('Below are team 1\'s cups:')
        print(cups_team_1)
        start_cup_amount_3 = cups_team_1.cup_count

        #determine if a player can and wants to rerack the cups
        if start_cup_amount_3 <=6 and start_cup_amount_3 > 1 and cups_team_1.reracks_remaining != 0:
            rerack_desired = input("Would you like to rerack your cups (Y/N)?")
            if rerack_desired == 'Y':
                type_of_rerack = input("What type of rerack would you like? ")
                cups_team_1.rerack(type_of_rerack)
                print("This is your new rack of cups!")
                print(cups_team_1)
            elif rerack_desired == 'N':
                continue
            else:
                raise Exception ('Please enter either Y or N.')

        aiming_cup_3 = int(input("Player 1 of team 1, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_1, team_1, player_1_team_1, aiming_cup_3)

        if cups_team_1.cup_count != start_cup_amount_3:
            take_drink(alc_type,player_1_team_2)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_1)

        #player 2 on team 1
        start_cup_amount_4 = cups_team_1.cup_count

        aiming_cup_4 = int(input("Player 2 of team 1, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_1, team_1, player_2_team_1, aiming_cup_4)

        if cups_team_1.cup_count != start_cup_amount_4:
            take_drink(alc_type, player_2_team_2)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_1)
        print('It\'s now team 2\'s turn')
        print('Below are team 2\'s cups: ')
        print(cups_team_2)

    #second half of loop if team 1 is starting
    else:
        #set counter for original number of cups
        start_cup_amount_1 = cups_team_1.cup_count

        #determine if a player can and wants to rerack the cups
        if start_cup_amount_1 <=6 and start_cup_amount_1 > 1 and cups_team_1.reracks_remaining != 0:
            rerack_desired = input("Would you like to rerack your cups (Y/N)?")
            if rerack_desired == 'Y':
                type_of_rerack = input("What type of rerack would you like? ")
                cups_team_1.rerack(type_of_rerack)
                print("This is your new rack of cups!")
                print(cups_team_1)
            elif rerack_desired == 'N':
                continue
            else:
                raise Exception ('Please enter either Y or N.')

        #determine aiming cup and throw ball
        aiming_cup_3 = int(input("Player 1 of team 1, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_1, team_1, player_1_team_1, aiming_cup_3)

        #make opposing player take a drink if a cup was hit
        if cups_team_1.cup_count != start_cup_amount_1:
            take_drink(alc_type,player_1_team_2)

        #see if ball is dented after that throw and print output of cups
        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_1)

        #repeat the above steps for all other players
        #player 2 on team 1
        start_cup_amount_2 = cups_team_1.cup_count

        aiming_cup_4 = int(input("Player 2 of team 1, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_1, team_1, player_2_team_1, aiming_cup_4)

        if cups_team_1.cup_count != start_cup_amount_2:
            take_drink(alc_type,player_2_team_2)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_1)

        #break out of loop if team 1 won
        if cups_team_1.cup_count == 0:
            break

        #player 1 on team 2
        print('It\'s now team 2\'s turn')
        print('Below are team 2\'s cups: ')
        print(cups_team_2)
        start_cup_amount_3 = cups_team_2.cup_count

        #determine if a player can and wants to rerack the cups
        if start_cup_amount_3 <=6 and start_cup_amount_3 > 1 and cups_team_2.reracks_remaining != 0:
            rerack_desired = input("Would you like to rerack your cups (Y/N)?")
            if rerack_desired == 'Y':
                type_of_rerack = input("What type of rerack would you like? ")
                cups_team_2.rerack(type_of_rerack)
                print("This is your new rack of cups!")
                print(cups_team_2)
            elif rerack_desired == 'N':
                continue
            else:
                raise Exception ('Please enter either Y or N.')

        aiming_cup_1 = int(input("Player 1 of team 2, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_2, team_2, player_1_team_2, aiming_cup_1)

        if cups_team_2.cup_count != start_cup_amount_3:
            take_drink(alc_type,player_1_team_1)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_2)

        #player 2 on team 2
        start_cup_amount_4 = cups_team_2.cup_count

        aiming_cup_2 = int(input("Player 2 of team 2, enter a cup position to aim at: "))
        throw_ball(ball, cups_team_2, team_2, player_2_team_2, aiming_cup_2)

        if cups_team_2.cup_count != start_cup_amount_4:
            take_drink(alc_type,player_2_team_1)

        dent_ball(ball,cups_team_1,cups_team_2)
        print(cups_team_2)
        print('It\'s now team 1\'s turn')
        print('Below are team 1\'s cups: ')
        print(cups_team_1)

#print who wins the game
if cups_team_2.cup_count == 0:
    print("Congratulations! Team 2 wins!")
else:
    print("Congratulations! Team 1 wins!")
