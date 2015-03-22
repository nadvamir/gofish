from unittest import TestCase
from mock import Mock 
from django.test import Client

c = Client()

class RegressionTest(TestCase):
    # test getting the list of levels
    def test_levels(self):
        response = c.get('/gofish/api/v2/home/').content
        self.assertTrue('"levels": [{' in response)

    # test getting the player information
    def test_player(self):
        response = c.get('/gofish/api/v2/player/').content
        self.assertTrue('"player":' in response)
        self.assertTrue('"money":' in response)
        self.assertTrue('"lineN":' in response)
        self.assertTrue('"cueN":' in response)
        self.assertTrue('"line":' in response)
        self.assertTrue('"cue":' in response)
        self.assertTrue('"boat":' in response)

    # test shop works
    def test_shop(self):
        shop = '''{"boats": [{"perk": "It floats.", "cost": 0, "name": "Raft"}, {"perk": "<span>67.0%</span> faster than a Raft", "cost": 500, "name": "Row Boat"}, {"perk": "<span>50.0%</span> faster than a Row Boat", "cost": 6000, "name": "Motor Boat"}, {"perk": "<span>50.0%</span> faster than a Motor Boat", "cost": 24000, "name": "Speed Boat"}], "cues": [{"perk": "You can't quite see underwater...", "cost": 0, "name": "Your Eyes"}, {"perk": "It shows you how deep water is", "cost": 30, "name": "A Map"}, {"perk": "It shows fish up to <span>4</span> tiles below you with a <span>50%</span> accuracy", "cost": 350, "name": "Underwater Camera"}, {"perk": "It shows fish up to <span>7</span> tiles below you with a <span>70%</span> accuracy", "cost": 1000, "name": "Old Sonar"}, {"perk": "It shows fish up to <span>10</span> tiles below you with a <span>85%</span> accuracy", "cost": 6200, "name": "Modern Sonar"}, {"perk": "It shows fish up to <span>10</span> tiles below you with a <span>100%</span> accuracy", "cost": 30000, "name": "A Mermaid"}], "lines": [{"perk": "Found in the attic.", "cost": 0, "name": "Old Fishing Line"}, {"perk": "<span>10.0%</span> more fish!", "cost": 1000, "name": "Strong Line"}, {"perk": "<span>20.0%</span> more fish!", "cost": 2000, "name": "Braided Line"}]}'''
        response = c.get('/gofish/api/v2/shop/').content
        self.assertEqual(shop, response)

    # test trophies call works
    def test_trophies(self):
        response = c.get('/gofish/api/v2/trophies/').content
        self.assertTrue('"gameTrophies": [' in response)
        self.assertTrue('"userTrophies": [' in response)

    # test there is no game until we create one
    def test_game_absence(self):
        response = c.get('/gofish/api/v2/game/').status_code
        self.assertEqual(404, response)

    #############################################################
    # usage scenarios
    #############################################################
    # balanced
    def test_simpleGame(self):
        self.startNewGame()
        [self.catchNext() for i in range(6)]
        self.moveRight(1)
        [self.catchNext() for i in range(6)]
        self.moveRight(2)
        [self.catchNext() for i in range(6)]
        self.moveRight(3)
        [self.catchNext() for i in range(6)]
        self.moveRight(4)
        [self.catchNext() for i in range(6)]
        self.moveRight(5)
        [self.catchNext() for i in range(6)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    # all in one go
    def test_allInOneGame(self):
        self.startNewGame()
        [self.catchNext() for i in range(96)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    # just move
    def test_justMove(self):
        self.startNewGame()
        [self.moveRight(i+1) for i in range(8)]
        self.failToMove()
        self.failToCatch()
        self.endGame()

    #############################################################
    # usage scenarios helpers
    #############################################################
    # start new game
    def startNewGame(self):
        newGame = c.get('/gofish/api/start/0/').content
        self.assertTrue('"money"' in newGame)
        self.assertTrue('"caught": []' in newGame)
        self.assertTrue('"cues": 0' in newGame)
        self.assertTrue('"level"' in newGame)
        self.assertTrue('"totalTime"' in newGame)
        self.assertTrue('"map"' in newGame)
        self.assertTrue('"fish"' in newGame)
        self.assertTrue('"timeInLoc"' in newGame)
        self.assertTrue('"yields"' in newGame)
        self.assertTrue('"time"' in newGame)

    # catch the next thing in yield
    def catchNext(self):
        catch = c.get('/gofish/api/action/catchall/1/').content
        self.assertTrue('"fishList"' in catch)
        self.assertTrue('"fishList": []' not in catch)
        self.assertTrue('"cues"' in catch)
        self.assertTrue('"time"' in catch)

    # fail to catch
    def failToCatch(self):
        catch = c.get('/gofish/api/action/catchall/1/').content
        # apparently, we do not fail, just ignore the request
        noCatch = '{"fishList": [], "cues": 0, "time": 480}'
        self.assertEqual(catch, noCatch)

    # move right
    def moveRight(self, newPos):
        move = c.get('/gofish/api/action/move/right/').content
        self.assertTrue('"position": ' + str(newPos) in move)
        self.assertTrue('"cues"' in move)
        self.assertTrue('"time"' in move)

    # fail to move
    def failToMove(self):
        move = c.get('/gofish/api/action/move/right/').content
        self.assertTrue('"error"' in move)

    # ending the game
    def endGame(self):
        end = c.get('/gofish/api/end/').content
        self.assertTrue('"money"' in end)
        self.assertTrue('"avg"' in end)
        self.assertTrue('"maximum"' in end)
        self.assertTrue('"stars"' in end)
        self.assertTrue('"earned"' in end)

