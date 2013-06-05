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

        self.playFields = self.createPlayField()
        self.fields = [item for sublist in self.playFields for item in sublist]

        self.selectedField = None
        self.firstSelected = None
        
    def handleClick(self, field):
        if (self.firstSelected is None):
            self.firstSelected = field
            
            if field.piece is not None:
                self.firstSelected = field

                if field.piece.type is 'F':
                    self.firstSelected = None
                    print ('Flag')

                if field.piece.type is 'B':
                    self.firstSelected = None
                    print ('Bom')
                
                if field.piece.type is '#':
                    self.firstSelected = None
                    print ('Blok')

        elif (self.firstSelected is not None):    
            # self.firstSelected = None

            if (field is not None):
                if (field.piece is None):
                    field.piece = self.firstSelected.piece
                    self.firstSelected.piece = None

                else:
                    if field.piece.type == '#':
                        print('blokkade')

                    if self.firstSelected.piece.type == 1:
                        if field.piece.type == 10:
                            print('Spy =D')
                            field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                            self.firstSelected.piece = None
                    
                    elif self.firstSelected.piece.type == 3:
                        if field.piece.type == 'B':
                            print ('Byebye Bom')
                            field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                            self.firstSelected.piece = None
                    
                    elif field.piece.type == 'F':
                        field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                        self.firstSelected.piece = None
                        print ('You Win')
                    
                    elif self.firstSelected.piece.type > field.piece.type:

                        field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                        self.firstSelected.piece = None
                        print ('Win')
                    
                    elif field.piece.type == (''):
                        field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
                        self.firstSelected.piece = None
                        print('leeg')
                    
                    elif self.firstSelected.piece.type < field.piece.type:
                        self.firstSelected.piece = None
                        print('Lose')
                    
                    elif self.firstSelected.piece.type == field.piece.type:
                        field.piece = None
                        self.firstSelected.piece = None
                        print ('Draw')




        # if field.selected:
        #     field.selected = False

        #     if self.firstSelected is None:
        #         if field.piece.type != '':
        #             self.firstSelected = field

        #         if field.piece.type is'F':
        #             self.firstSelected = None
        #             print ('Flag')

        #         if field.piece.type is'B':
        #             self.firstSelected = None
        #             print ('Bom')
                
        #         if field.piece.type is '#':
        #             self.firstSelected = None
        #             print ('Blok')

        # else:
        #     done = True

        #     if done:
        #         if field.piece.type == '#':
        #             print('blokkade')
        #             done = False
        #     if done:
        #         if self.firstSelected.piece.type == 1:
        #             if field.piece.type == 10:
        #                 print('Spy =D')
        #                 field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
        #                 self.firstSelected.piece = Piece('', 0)
        #                 done = False
        #     if done:
        #         if self.firstSelected.piece.type == 3:
        #             if field.piece.type == 'B':
        #                 print ('Byebye Bom')
        #                 field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
        #                 self.firstSelected.piece = Piece('', 0)
        #                 done = False
        #     if done:
        #         if field.piece.type == 'F':
        #             field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
        #             self.firstSelected.piece = Piece('', 0)
        #             print ('You Win')
        #             done = False
        #     if done:

        #         if self.firstSelected.piece.type > field.piece.type:

        #             field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
        #             self.firstSelected.piece = Piece('', 0)
        #             done = False
        #             print ('Win')
        #     if done:
        #         if field.piece.type == (''):
        #             field.piece = Piece(self.firstSelected.piece.type, self.firstSelected.piece.steps)
        #             self.firstSelected.piece = Piece('', 0)
        #             print('leeg')
        #             done = False
        #     if done:
        #         if self.firstSelected.piece.type < field.piece.type:
        #             self.firstSelected.piece = Piece('', 0)
        #             done = False
        #             print('Lose')
        #     if done:
        #         if self.firstSelected.piece.type == field.piece.type:
        #             field.piece = Piece('', 0)
        #             self.firstSelected.piece = Piece('', 0)
        #             done = False
        #             print ('Draw')

            self.firstSelected = None

    def createPlayField(self):
        playFields = [[Field(0, 0, self.sizeOfField) for x in xrange(self.widthOfField)] for y in xrange(self.heightOfField)]

        for y in range(len(playFields)):
            for x in range(len(playFields[0])):
                playFields[y][x].x = x * playFields[y][x].size*2 + self.xOffset + self.fieldOffset * x
                playFields[y][x].y = y * playFields[y][x].size*2 + self.yOffset + self.fieldOffset * y
                
                if (y in range(4)):
                    playFields[y][x].piece = self.player1.pieces[y][x]

                if (y in range(6, 10)):
                    playFields[y][x].piece = self.player2.pieces[y-6][x]

                try:
                    self.barrierFields.index([x, y])
                except ValueError:
                    pass
                else:
                    playFields[y][x].barrier = True
                    playFields[y][x].piece = Piece('#', 0)

        return playFields

    def draw(self):

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
        # Draw playFields
        for y in range(0, len(self.playFields)):
            for x in range(0, len(self.playFields[y])):
                field = self.playFields[y][x]


                if (field.barrier):
                    glColor3f(1, 0, 0)
                elif (self.firstSelected is field):
                    glColor3f(1, 0, 1)
                else:
                    glColor3f(1, 1, 1)

                Drawer.drawField(field)
