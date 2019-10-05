import unittests
import minolovec

class TestGame(unittest.TestCase):
    def setUp(self,*args):
        self.game = minolovec.Mineswepper(args)
		
	def test_info(self):
        odkje = self.game.odkje
        self.assertTrue(odkje==False)