from pygame.sprite import Sprite
import pygame
import sys
import SocketServer, struct
# import re

screen = None #setting them as global for now, may be better solution
ball = None
ballrect = None
paddle_left = None #these should be in array, just trying to make it work for now
paddle_left_rect = None
paddle_right = None
paddle_right_rect = None
boundsx = [None, None] #left, right
boundsy = [None, None] #top, bottom
# right_edge_node = None
# left_edge_node = None
# ip_address = None
# paddle_index = 0
# ip_address = None

black = 0,0,0


class broadcastServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
class requestHandler(SocketServer.StreamRequestHandler):
    #currentUserLogin={} #{clientArr:accountName}
    def handle(self):
        global screen, ball, ballrect, paddle_left_rect, paddle_right_rect, bounds,\
            edge_node, paddle_index
        posvec=self.request.recv(16)
        print(self.client_address)
        while posvec !='':
            pos = struct.unpack( 'iiii',posvec )
            #print( pos )
            ballrect.x = pos[0] - boundsx[0] # offset the bounds
            ballrect.y = pos[1] - boundsy[0] 
            # print "ball postition"
            # print "x= " + str(ballrect.x)
            # print "y= " +str(ballrect.y)
            # print "center = " + str(ballrect.center)
            # print "top = " +str(ballrect.top)
            # print "bottom = " + str(ballrect.bottom)
            # print "left = " + str(ballrect.left)
            # print "right = " + str(ballrect.right)
            # print "topleft = " + str(ballrect.topleft)
            #print( pos[2], pos[3] )
            screen.fill( black )
            if ( pos[0] > boundsx[0] and pos[1] < boundsx[1] ):
                screen.blit( ball, ballrect )
            #don't care for now but will have to figure out what to do after
            # screen.blit( paddle_right, paddle_right_rect )
            if edge_node:
                if ( pos[paddle_index] > boundsy[0] and pos[paddle_index] < boundsy[1]  ):
                    paddle_rect.y = pos[paddle_index] - boundsy[0]
                    screen.blit( paddle, paddle_rect )
            pygame.display.flip()
            self.request.send( 'Got it' )
            try:
                posvec=self.request.recv( 16 )
            except:
                print( 'client disconnect' )
                pygame.quit()
                sys.exit()
        pygame.quit()
        sys.exit()

def read_pong_settings():
    # put in seperate function since it's special. Could have been done easier
    global  boundx, boundsy, right_edge_node, left_edge_node, ip_address
    settings = open( 'settings.txt', 'r' )
    line = settings.readline()
    boundsx[0] = int( settings.readline().strip() ) 
    print boundsx[0]
    line = settings.readline()
    boundsx[1] = int( settings.readline().strip() )
    print boundsx[1]
    line = settings.readline()
    boundsy[0] = int( settings.readline().strip() ) 
    print boundsy[0]
    line = settings.readline()
    boundsy[1] = int( settings.readline().strip() )
    print boundsy[1]
    line = settings.readline()
    right_edge_node = settings.readline().strip() 
    print right_edge_node
    line = settings.readline()
    left_edge_node = settings.readline().strip() 
    print left_edge_node
    line = settings.readline()
    ip_address = settings.readline().strip()
    print ip_address
    settings.close()

if __name__ == '__main__':
    #global edge_node, paddle, right_edge_node, left_edge_node, paddle_rect,\
     #   paddle_index
    pygame.init()
    screen = pygame.display.set_mode( (1360,768) )
    ball = pygame.image.load( 'assets/ball.png' )
    ballrect = ball.get_rect()
    read_pong_settings()
    if ( right_edge_node == 'True' ):
        print ";asd"
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 1276
        edge_node = True #will signal to update paddle as well
        paddle_index = 3
    elif( left_edge_node == 'True' ):
        print 'sddf'
        paddle = pygame.image.load( 'assets/paddle.png' )
        paddle_rect = paddle.get_rect()
        paddle_rect.x = 84
        edge_node = True #will signal to update paddle as well
        paddle_index = 2
    print ip_address
    server=broadcastServer( ( ip_address, 20000 ), requestHandler )
    server.serve_forever()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
    
        
        