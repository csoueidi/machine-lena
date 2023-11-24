# Generated from choreography/Choreography.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,88,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,4,0,26,8,0,11,
        0,12,0,27,1,1,1,1,1,1,1,1,1,1,3,1,35,8,1,1,2,1,2,1,2,1,2,3,2,41,
        8,2,1,2,1,2,1,2,1,2,3,2,47,8,2,1,2,1,2,1,3,1,3,1,3,4,3,54,8,3,11,
        3,12,3,55,1,3,1,3,1,4,1,4,1,4,1,4,4,4,64,8,4,11,4,12,4,65,1,4,1,
        4,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,
        10,1,11,1,11,1,11,0,0,12,0,2,4,6,8,10,12,14,16,18,20,22,0,1,1,0,
        12,13,84,0,25,1,0,0,0,2,34,1,0,0,0,4,36,1,0,0,0,6,50,1,0,0,0,8,59,
        1,0,0,0,10,69,1,0,0,0,12,72,1,0,0,0,14,77,1,0,0,0,16,79,1,0,0,0,
        18,81,1,0,0,0,20,83,1,0,0,0,22,85,1,0,0,0,24,26,3,2,1,0,25,24,1,
        0,0,0,26,27,1,0,0,0,27,25,1,0,0,0,27,28,1,0,0,0,28,1,1,0,0,0,29,
        35,3,4,2,0,30,35,3,6,3,0,31,35,3,8,4,0,32,35,3,10,5,0,33,35,3,12,
        6,0,34,29,1,0,0,0,34,30,1,0,0,0,34,31,1,0,0,0,34,32,1,0,0,0,34,33,
        1,0,0,0,35,3,1,0,0,0,36,37,5,1,0,0,37,40,5,2,0,0,38,41,5,3,0,0,39,
        41,3,14,7,0,40,38,1,0,0,0,40,39,1,0,0,0,41,42,1,0,0,0,42,43,5,4,
        0,0,43,46,3,16,8,0,44,45,5,4,0,0,45,47,3,18,9,0,46,44,1,0,0,0,46,
        47,1,0,0,0,47,48,1,0,0,0,48,49,5,5,0,0,49,5,1,0,0,0,50,51,5,6,0,
        0,51,53,5,7,0,0,52,54,3,4,2,0,53,52,1,0,0,0,54,55,1,0,0,0,55,53,
        1,0,0,0,55,56,1,0,0,0,56,57,1,0,0,0,57,58,5,8,0,0,58,7,1,0,0,0,59,
        60,5,9,0,0,60,61,3,22,11,0,61,63,5,7,0,0,62,64,3,2,1,0,63,62,1,0,
        0,0,64,65,1,0,0,0,65,63,1,0,0,0,65,66,1,0,0,0,66,67,1,0,0,0,67,68,
        5,8,0,0,68,9,1,0,0,0,69,70,5,10,0,0,70,71,3,18,9,0,71,11,1,0,0,0,
        72,73,5,11,0,0,73,74,5,2,0,0,74,75,3,20,10,0,75,76,5,5,0,0,76,13,
        1,0,0,0,77,78,5,12,0,0,78,15,1,0,0,0,79,80,7,0,0,0,80,17,1,0,0,0,
        81,82,7,0,0,0,82,19,1,0,0,0,83,84,7,0,0,0,84,21,1,0,0,0,85,86,5,
        12,0,0,86,23,1,0,0,0,6,27,34,40,46,55,65
    ]

class ChoreographyParser ( Parser ):

    grammarFileName = "Choreography.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'move'", "'('", "'all'", "','", "')'", 
                     "'sync'", "'{'", "'}'", "'repeat'", "'set_frps'", "'wait'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "INTEGER", "DECIMAL", "COMMENT", "WS" ]

    RULE_choreography = 0
    RULE_command = 1
    RULE_moveCommand = 2
    RULE_syncCommand = 3
    RULE_repeatCommand = 4
    RULE_setFrpsCommand = 5
    RULE_waitCommand = 6
    RULE_motor = 7
    RULE_degree = 8
    RULE_speed = 9
    RULE_seconds = 10
    RULE_times = 11

    ruleNames =  [ "choreography", "command", "moveCommand", "syncCommand", 
                   "repeatCommand", "setFrpsCommand", "waitCommand", "motor", 
                   "degree", "speed", "seconds", "times" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    INTEGER=12
    DECIMAL=13
    COMMENT=14
    WS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ChoreographyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def command(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ChoreographyParser.CommandContext)
            else:
                return self.getTypedRuleContext(ChoreographyParser.CommandContext,i)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_choreography

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChoreography" ):
                return visitor.visitChoreography(self)
            else:
                return visitor.visitChildren(self)




    def choreography(self):

        localctx = ChoreographyParser.ChoreographyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_choreography)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 24
                self.command()
                self.state = 27 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 3650) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def moveCommand(self):
            return self.getTypedRuleContext(ChoreographyParser.MoveCommandContext,0)


        def syncCommand(self):
            return self.getTypedRuleContext(ChoreographyParser.SyncCommandContext,0)


        def repeatCommand(self):
            return self.getTypedRuleContext(ChoreographyParser.RepeatCommandContext,0)


        def setFrpsCommand(self):
            return self.getTypedRuleContext(ChoreographyParser.SetFrpsCommandContext,0)


        def waitCommand(self):
            return self.getTypedRuleContext(ChoreographyParser.WaitCommandContext,0)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_command

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommand" ):
                return visitor.visitCommand(self)
            else:
                return visitor.visitChildren(self)




    def command(self):

        localctx = ChoreographyParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_command)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.moveCommand()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 30
                self.syncCommand()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 31
                self.repeatCommand()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 4)
                self.state = 32
                self.setFrpsCommand()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 5)
                self.state = 33
                self.waitCommand()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MoveCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def degree(self):
            return self.getTypedRuleContext(ChoreographyParser.DegreeContext,0)


        def motor(self):
            return self.getTypedRuleContext(ChoreographyParser.MotorContext,0)


        def speed(self):
            return self.getTypedRuleContext(ChoreographyParser.SpeedContext,0)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_moveCommand

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMoveCommand" ):
                return visitor.visitMoveCommand(self)
            else:
                return visitor.visitChildren(self)




    def moveCommand(self):

        localctx = ChoreographyParser.MoveCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_moveCommand)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(ChoreographyParser.T__0)
            self.state = 37
            self.match(ChoreographyParser.T__1)
            self.state = 40
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.state = 38
                self.match(ChoreographyParser.T__2)
                pass
            elif token in [12]:
                self.state = 39
                self.motor()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 42
            self.match(ChoreographyParser.T__3)
            self.state = 43
            self.degree()
            self.state = 46
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 44
                self.match(ChoreographyParser.T__3)
                self.state = 45
                self.speed()


            self.state = 48
            self.match(ChoreographyParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SyncCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def moveCommand(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ChoreographyParser.MoveCommandContext)
            else:
                return self.getTypedRuleContext(ChoreographyParser.MoveCommandContext,i)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_syncCommand

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSyncCommand" ):
                return visitor.visitSyncCommand(self)
            else:
                return visitor.visitChildren(self)




    def syncCommand(self):

        localctx = ChoreographyParser.SyncCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_syncCommand)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(ChoreographyParser.T__5)
            self.state = 51
            self.match(ChoreographyParser.T__6)
            self.state = 53 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 52
                self.moveCommand()
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 57
            self.match(ChoreographyParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RepeatCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def times(self):
            return self.getTypedRuleContext(ChoreographyParser.TimesContext,0)


        def command(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ChoreographyParser.CommandContext)
            else:
                return self.getTypedRuleContext(ChoreographyParser.CommandContext,i)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_repeatCommand

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRepeatCommand" ):
                return visitor.visitRepeatCommand(self)
            else:
                return visitor.visitChildren(self)




    def repeatCommand(self):

        localctx = ChoreographyParser.RepeatCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_repeatCommand)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(ChoreographyParser.T__8)
            self.state = 60
            self.times()
            self.state = 61
            self.match(ChoreographyParser.T__6)
            self.state = 63 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 62
                self.command()
                self.state = 65 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 3650) != 0)):
                    break

            self.state = 67
            self.match(ChoreographyParser.T__7)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetFrpsCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def speed(self):
            return self.getTypedRuleContext(ChoreographyParser.SpeedContext,0)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_setFrpsCommand

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetFrpsCommand" ):
                return visitor.visitSetFrpsCommand(self)
            else:
                return visitor.visitChildren(self)




    def setFrpsCommand(self):

        localctx = ChoreographyParser.SetFrpsCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_setFrpsCommand)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(ChoreographyParser.T__9)
            self.state = 70
            self.speed()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WaitCommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def seconds(self):
            return self.getTypedRuleContext(ChoreographyParser.SecondsContext,0)


        def getRuleIndex(self):
            return ChoreographyParser.RULE_waitCommand

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWaitCommand" ):
                return visitor.visitWaitCommand(self)
            else:
                return visitor.visitChildren(self)




    def waitCommand(self):

        localctx = ChoreographyParser.WaitCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_waitCommand)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(ChoreographyParser.T__10)
            self.state = 73
            self.match(ChoreographyParser.T__1)
            self.state = 74
            self.seconds()
            self.state = 75
            self.match(ChoreographyParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MotorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(ChoreographyParser.INTEGER, 0)

        def getRuleIndex(self):
            return ChoreographyParser.RULE_motor

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMotor" ):
                return visitor.visitMotor(self)
            else:
                return visitor.visitChildren(self)




    def motor(self):

        localctx = ChoreographyParser.MotorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_motor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(ChoreographyParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DegreeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(ChoreographyParser.DECIMAL, 0)

        def INTEGER(self):
            return self.getToken(ChoreographyParser.INTEGER, 0)

        def getRuleIndex(self):
            return ChoreographyParser.RULE_degree

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDegree" ):
                return visitor.visitDegree(self)
            else:
                return visitor.visitChildren(self)




    def degree(self):

        localctx = ChoreographyParser.DegreeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_degree)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            _la = self._input.LA(1)
            if not(_la==12 or _la==13):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpeedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(ChoreographyParser.DECIMAL, 0)

        def INTEGER(self):
            return self.getToken(ChoreographyParser.INTEGER, 0)

        def getRuleIndex(self):
            return ChoreographyParser.RULE_speed

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSpeed" ):
                return visitor.visitSpeed(self)
            else:
                return visitor.visitChildren(self)




    def speed(self):

        localctx = ChoreographyParser.SpeedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_speed)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            _la = self._input.LA(1)
            if not(_la==12 or _la==13):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SecondsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(ChoreographyParser.DECIMAL, 0)

        def INTEGER(self):
            return self.getToken(ChoreographyParser.INTEGER, 0)

        def getRuleIndex(self):
            return ChoreographyParser.RULE_seconds

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeconds" ):
                return visitor.visitSeconds(self)
            else:
                return visitor.visitChildren(self)




    def seconds(self):

        localctx = ChoreographyParser.SecondsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_seconds)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not(_la==12 or _la==13):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(ChoreographyParser.INTEGER, 0)

        def getRuleIndex(self):
            return ChoreographyParser.RULE_times

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimes" ):
                return visitor.visitTimes(self)
            else:
                return visitor.visitChildren(self)




    def times(self):

        localctx = ChoreographyParser.TimesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_times)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(ChoreographyParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





