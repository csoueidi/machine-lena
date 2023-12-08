# Generated from Choreography.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ChoreographyParser import ChoreographyParser
else:
    from ChoreographyParser import ChoreographyParser

# This class defines a complete generic visitor for a parse tree produced by ChoreographyParser.

class ChoreographyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ChoreographyParser#choreography.
    def visitChoreography(self, ctx:ChoreographyParser.ChoreographyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#command.
    def visitCommand(self, ctx:ChoreographyParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#moveCommand.
    def visitMoveCommand(self, ctx:ChoreographyParser.MoveCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#syncCommand.
    def visitSyncCommand(self, ctx:ChoreographyParser.SyncCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#repeatCommand.
    def visitRepeatCommand(self, ctx:ChoreographyParser.RepeatCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#setFrpsCommand.
    def visitSetFrpsCommand(self, ctx:ChoreographyParser.SetFrpsCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#waitCommand.
    def visitWaitCommand(self, ctx:ChoreographyParser.WaitCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#motor.
    def visitMotor(self, ctx:ChoreographyParser.MotorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#degree.
    def visitDegree(self, ctx:ChoreographyParser.DegreeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#speed.
    def visitSpeed(self, ctx:ChoreographyParser.SpeedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#seconds.
    def visitSeconds(self, ctx:ChoreographyParser.SecondsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ChoreographyParser#times.
    def visitTimes(self, ctx:ChoreographyParser.TimesContext):
        return self.visitChildren(ctx)



del ChoreographyParser