from pyparsing import *
import sys

class SL0Parser:

	def __init__(self):

		lpar = Literal("(").suppress()
		rpar = Literal(")").suppress()
		

		word = ~Literal(":")+ Word(alphanums+"-_@./\\:")
		StringLiteral = Combine( Literal('"') + ZeroOrMore( CharsNotIn('\"') | ( Literal('\\"') ) ) + Literal('"') ).streamline()
		String = ( word | StringLiteral )     #| ByteLengthEncodedString )
		Constant = String
		
		Key = String
		Expr = Forward()
		Parameter =  Dict(Group(Literal(":").suppress() + Key + Group(Constant|Expr)))
		Expr << Dict(Group( lpar + Key + Group(OneOrMore(Parameter)|OneOrMore(Constant)|OneOrMore(Expr)) + rpar ))



		Content = ( lpar + OneOrMore(Expr) + rpar )

 
		self.bnf = Content

		#self.bnf.setDebug()

		try:
			#self.bnf.validate()
			pass

		except Exception, err:
			print err
			sys.exit(-1)
		



	def parse(self,string):

		try:
			m = self.bnf.parseString(string)
		except ParseException, err:
			print err.line
			print " "*(err.column-1)+"|"
			print err
			sys.exit(-1)
		except Exception, err:
			print "Unkwonw Exception"
			print err
			sys.exit(-1)

		return m

	def parseFile(self,file):

		try:
			m = self.bnf.parseFile(file)
		except ParseException, err:
			print err.line
			print " "*(err.column-1)+"|"
			print err
			sys.exit(-1)
		except Exception, err:
			print "Unkwonw Exception"
			print err
			sys.exit(-1)

		return m

if __name__ == "__main__":
	p = SL0Parser()
	msg = p.parse("((prueba :name (set (bla uno) (bla dos))))")
	#msg = p.parseFile("message.sl0")
	#print repr(msg)
	print msg.asXML()
	print msg.asList()
	#print "--------------------"
	#print msg.action['agent-identifier'].addresses.keys()
	#print msg.action['agent-identifier'].addresses.sequence[1]

	print msg.prueba.name.set
	print msg.prueba.name.set.bla
	print msg.prueba.name.set.bla.keys()
	print msg.prueba.name.set.bla.values()
	print msg.prueba.name.set.bla[0]
	print "--"
	print msg.prueba.name.set.values()
	print "--"
