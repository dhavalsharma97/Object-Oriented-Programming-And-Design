//RED ID: 824654344
//[Node.java]
//Class for implementing a node in the circular doubly linked queue
class Node
{
	protected Process data;
	protected Node successor, predecessor;
	
	//Default constructor for initializing the fields of class Node
	public Node()
	{
		data = null;
		successor = null;
		predecessor = null;
	}
	
	//Parameterized Constructor for initializing the fields of class Node
	public Node(Process newData, Node newSuccessor, Node newPredecessor)
	{
		data = newData;
		successor = newSuccessor;
		predecessor = newPredecessor;
	}
}