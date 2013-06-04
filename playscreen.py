import pyglet
from pyglet.gl import *
from field import Field
from piece import Piece
from drawer import Drawer

class PlayScreen:

    def __init__(self, window, player1, player2):
        self.window = window
        self.xOffset = self.window.get_size()[0]/4
        self.yOffset = self.window.get_size()[1]/8 + 35
        self.fieldOffset = 1
        self.barrierFields = [[2, 4], [3, 4], [6, 4], [7, 4], [2, 5], [3, 5], [6, 5], [7, 5]]

        self.player1 = player1
        self.player1Pieces = player1.pieces
        self.player2 = player2
        self.player2Pieces = player2.pieces

        self.widthOfField = 10
        self.heightOfField = 10
        self.sizeOfField = 25
        self.isFieldSelected = False
        self.selectedField = 0
        self.color = [1, 1, 1]
        self.fields = self.createPlayField()
        self.selectedField = None
        self.firstSelected = None
        
        

    def createPlayField(self):
        fields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(0, len(fields)):
            for x in range(0, len(fields[0])):
                fields[y][x].x = x * fields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                fields[y][x].y = y * fields[y][x].size*2 + self.yOffset + self.fieldOffset * y
                
                if (y in range(3)):
                    fields[y][x].piece = self.player1.pieces[y*self.widthOfField+x]

                if (y in range(7, 10)):
                    fields[y][x].piece = self.player2.pieces[(y-6)*self.widthOfField+x]


                try:
                    self.barrierFields.index([x, y])
                except ValueError:
                    pass
                else:
                    fields[y][x].barrier = True
                    fields[y][x].piece = Piece('#', 0)

        return fields

    def draw(self):

        # Player 1's turn
        # if (self.window.whosTurn is 1):
        #     if (self.player1.isComputer is True):
        #         print "lolbbqsauce"
        # elif (self.window.whosTurn is 2):
        #      # Player 2's turn
        #     if (self.player2.isComputer is True):
        #         self.player2.play()

        pyglet.text.Label('Player 1',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=self.window.get_size()[1]-20,
                          anchor_x='center', anchor_y='center').draw()

        pyglet.text.Label('Player 2',
                          font_name='Arial',
                          font_size=16,
                          x=self.window.get_size()[0]/2, y=20,
                          anchor_x='center', anchor_y='center').draw()
        # Draw fields
        for y in range(0, len(self.fields)):
            for x in range(0, len(self.fields[y])):

                field = self.fields[y][x]
                if field.selected:

                    if self.firstSelected is None:
                        if field.piece.type != '':
                            self.firstSelected = field

                        if field.piece.type is'F':
                            self.firstSelected = None
                            print ('Flag')

                        if field.piece.type is'B':
                            self.firstSelected = None
                            print ('Bom')
                        if field.piece.type is '#':
                            self.firstSelected = None
                            print ('Blok')

                    else:
                        done = True

                        if done:
                            if field.piece.type == '#':
                                print('blokkade')
                                done = False
                        if done:
                            if self.firstSelected.piece.type == 1:
                                if field.piece.type == 10:
                                    print('Spy =D')
                                    field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                                    self.firstSelected.piece = Piece('', 0)
                                    done = False
                        if done:
                            if self.firstSelected.piece.type == 3:
                                if field.piece.type == 'B':
                                    print ('Byebye Bom')
                                    field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                                    self.firstSelected.piece = Piece('', 0)
                                    done = False
                        if done:
                            if field.piece.type == 'F':
                                field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                                self.firstSelected.piece = Piece('', 0)
                                print ('You Win')
                                done = False
                        if done:

                            if self.firstSelected.piece.type > field.piece.type:

                                field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                                self.firstSelected.piece = Piece('', 0)
                                done = False
                                print ('Win')
                        if done:
                            if field.piece.type == (''):
                                field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                                self.firstSelected.piece = Piece('', 0)
                                print('leeg')
                                done = False
                        if done:
                            if self.firstSelected.piece.type < field.piece.type:
                                self.firstSelected.piece = Piece('', 0)
                                done = False
                                print('Lose')
                        if done:
                            if self.firstSelected.piece.type == field.piece.type:
                                field.piece = Piece('', 0)
                                self.firstSelected.piece = Piece('', 0)
                                done = False
                                print ('Draw')

                        self.firstSelected = None

                field.selected = False

                if (field.barrier):
                    glColor3f(1, 0, 0)
                elif (self.firstSelected is field):
                    glColor3f(1, 0, 1)
                else:
                    glColor3f(1, 1, 1)

                Drawer.drawField(field)
