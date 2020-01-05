//RED ID: 824654344
//[CircularDoublyLinkedQueue.java]
//Class for implementing the circular doubly linked queue
class CircularDoublyLinkedQueue
{
	protected Node start;
	protected Node end;
	protected Node endNode;
	public int length;
	public int capacity;
	
	//Default constructor for initializing the fields of class CircularDoublyLinkedQueue
	public CircularDoublyLinkedQueue()
	{
		capacity = 2;
		length = 0;
		start = null;
		end = null;
		endNode = null;
	}
	
	//Function for adding empty node in the circular doubly linked queue
	public void addEmptyNode()
	{	
		Process emptyProcess = new Process();
		Node emptyNode = new Node(emptyProcess, null, null);
		
		//Checking to see if the circular doubly linked queue is empty?
		if(start == null)
		{
			emptyNode.successor = emptyNode;
			emptyNode.predecessor = emptyNode;
			start = emptyNode;
			end = emptyNode;
			endNode = emptyNode;
		}
		else
		{
			emptyNode.predecessor = endNode;
			endNode.successor = emptyNode;
			start.predecessor = emptyNode;
			emptyNode.successor = start;
			endNode = emptyNode;
		}
	}
	
	//Function for adding data to the node in the circular doubly linked queue
	public void addElement(Process newProcess)
	{
		//Checking to see whether the queue is full or not?
		if(length == capacity)
		{
			increaseCapacity();
		}
		
		//Checking to see if the circular doubly linked queue contains any elements?
		if(length == 0)
		{
			end.data = newProcess;
		}
		else
		{
			end = end.successor;
			end.data = newProcess;
		}
		length = length + 1;
	}
	
	//Function for removing a node from the circular doubly linked queue
	public Process removeElement()
	{
		Process deletedElement = new Process();
		deletedElement.setProcessAttributes(start.data.pid, start.data.name, start.data.owner, start.data.numOfThreads, start.data.cpuPercent, start.data.cpuTime);
		
		//Checking to see if the circular doubly linked queue is empty or not?
		if(length == 0)
		{
			return null;
		}
		else if(length == 1)
		{
			start = start.successor;
			end = start;
			endNode = start.predecessor;
			endNode.data.setProcessAttributes(0, null, null, 0, 0, 0);
			length = 0;
			return deletedElement;
		}
		else
		{
			start = start.successor;
			endNode = start.predecessor;
			endNode.data.setProcessAttributes(0, null, null, 0, 0, 0);
			length = length - 1;
			return deletedElement;
		}
	}
	
	//Function for doubling the capacity of the circular doubly linked queue
	public void increaseCapacity()
	{	
		for(int numOfNodes = 0; numOfNodes < capacity; numOfNodes++)
		{
			addEmptyNode();
		}
		capacity = capacity * 2;
	}
	
	//Function to display the data in the nodes according to the attributes in the circular doubly linked queue
	public void displaySortedQueue(String selectedAttribute)
	{
		if(length == 0)
		{
			System.out.println("The queue contains no elements!");
		}
		else
		{
			//Making an array containing the nodes of the circular doubly linked queue
			Node nodesArray[] = new Node[length];
			Node currentQueueNode = start;
			nodesArray[0] = currentQueueNode;
			for(int arrayCounter=1; arrayCounter<length; arrayCounter++)
			{
				currentQueueNode = currentQueueNode.successor;
				nodesArray[arrayCounter] = currentQueueNode;
			}
			
			//Sorting the nodesArray with respect to the selectedAttribute by using sortArrayOfNodes function of SortArray class
			SortArray sortArrayObj = new SortArray(selectedAttribute);
			sortArrayObj.sortArrayOfNodes(nodesArray, 0, nodesArray.length - 1);
			
			//Displaying the sorted array with the help of for loop
			for(int arrayDisplayCounter = 0; arrayDisplayCounter < nodesArray.length; arrayDisplayCounter++)
			{
				System.out.print("\n(" + (arrayDisplayCounter + 1) + ") ");
				nodesArray[arrayDisplayCounter].data.displayProcessAttributes();
			}
		}
	}

	//Function for displaying the circular doubly linked queue
	public void displayQueue()
	{
		System.out.println("\nThe current circular doubly linked queue:");
		Node currentNode = start;
		int counter = 1;
		
		System.out.print("(" + counter + ") ");
		currentNode.data.displayProcessAttributes();
		
		//Loop for traversing and printing the nodes in the circular doubly linked queue
		while(currentNode.successor != start)
		{
			counter = counter + 1;
			currentNode = currentNode.successor;
			System.out.print("\n(" + counter + ") ");
			currentNode.data.displayProcessAttributes();
		}	
	}
}