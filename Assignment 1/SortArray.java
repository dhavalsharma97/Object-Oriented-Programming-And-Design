//RED ID: 824654344
//[SortArray.java]
//Class for implementing the logic for sorting the array of nodes of the circular doubly linked queue
class SortArray
{
	protected String selectedAttribute;
	
	//Default constructor for initializing the value of the selectedAttribute to PID
	public SortArray()
	{
		selectedAttribute = "PID";
	}
	
	//Parameterized Constructor for initializing the value of the selectedAttribute equal to the parameter passed to it
	public SortArray(String newSelectedAttribute)
	{
		selectedAttribute = newSelectedAttribute;
	}
	
	//Function for merge sorting the array of nodes of the circular doubly linked queue
	public void sortArrayOfNodes(Node nodesArray[], int posOfLeftElement, int posOfRightElement)
	{
		if(posOfLeftElement < posOfRightElement)
		{
			int posOfMiddleElement = (posOfLeftElement + posOfRightElement) / 2;
			
			//Calling the function sortArrayOfNodes recursively by splitting the elements in the nodesArray
			sortArrayOfNodes(nodesArray, posOfLeftElement, posOfMiddleElement);
			sortArrayOfNodes(nodesArray, posOfMiddleElement + 1, posOfRightElement);
			
			//Calling the function mergeNodes to merge the nodes in the ascending order
			mergeNodes(nodesArray, posOfLeftElement, posOfMiddleElement, posOfRightElement);
		}
	}
	
	//Function for merging the nodes in the process of merge sort
	public void mergeNodes(Node nodesArray[], int posOfLeftElement, int posOfMiddleElement, int posOfRightElement)
	{
		//Initializing the leftArray and rightArray to hold half of the elements
		int sizeOfLeftArray = posOfMiddleElement - posOfLeftElement + 1;
		int sizeOfRightArray = posOfRightElement - posOfMiddleElement;
		Node leftArray[] = new Node[sizeOfLeftArray];
		Node rightArray[] = new Node[sizeOfRightArray];
		
		for(int leftArrayCounter = 0; leftArrayCounter < sizeOfLeftArray; ++leftArrayCounter)
		{
			leftArray[leftArrayCounter] = nodesArray[posOfLeftElement + leftArrayCounter];		
		}
		
		for(int rightArrayCounter = 0; rightArrayCounter < sizeOfRightArray; ++rightArrayCounter)
		{
			rightArray[rightArrayCounter] = nodesArray[posOfMiddleElement + 1 + rightArrayCounter];
		}
		
		//Starting to merge the nodes with respect to the selectedAttribute
		int leftArrayPointer = 0, rightArrayPointer = 0, currentElementPointer = posOfLeftElement;
		while(leftArrayPointer < sizeOfLeftArray && rightArrayPointer < sizeOfRightArray)
		{
			if(sortByAttribute(leftArray[leftArrayPointer], rightArray[rightArrayPointer]))
			{
				nodesArray[currentElementPointer] = leftArray[leftArrayPointer];
				leftArrayPointer++;
			}
			else
			{
				nodesArray[currentElementPointer] = rightArray[rightArrayPointer];
				rightArrayPointer++;
			}
			currentElementPointer++;
		}
		
		//Inserting the remaining elements from the leftArray to the nodesArray
		while(leftArrayPointer < sizeOfLeftArray)
		{
			nodesArray[currentElementPointer] = leftArray[leftArrayPointer];
			leftArrayPointer++;
			currentElementPointer++;
		}
		
		//Inserting the remaining elements from the RightArray to the nodesArray
		while(rightArrayPointer < sizeOfRightArray)
		{
			nodesArray[currentElementPointer] = rightArray[rightArrayPointer];
			rightArrayPointer++;
			currentElementPointer++;
		}
	}
	
	//Function for sorting the elements in the nodesArray according to the selectedAttribute
	public boolean sortByAttribute(Node leftElement, Node rightElement)
	{
		switch(selectedAttribute.toLowerCase())
		{
			case "pid":
				if(leftElement.data.pid <= rightElement.data.pid)
				{
					return true;
				}
				else
				{
					return false;
				}
			case "name":
				if(leftElement.data.name.toLowerCase().compareTo(rightElement.data.name.toLowerCase()) <= 0)
				{
					return true;
				}
				else
				{
					return false;
				}
			case "owner":
				if(leftElement.data.owner.toLowerCase().compareTo(rightElement.data.owner.toLowerCase()) <= 0)
				{
					return true;
				}
				else
				{
					return false;
				}
			case "numberofthreads":
				if(leftElement.data.numOfThreads <= rightElement.data.numOfThreads)
				{
					return true;
				}
				else
				{
					return false;
				}
			case "cpupercent":
				if(leftElement.data.cpuPercent <= rightElement.data.cpuPercent)
				{
					return true;
				}
				else
				{
					return false;
				}
			case "cputime":
				if(leftElement.data.cpuTime <= rightElement.data.cpuTime)
				{
					return true;
				}
				else
				{
					return false;
				}
			default:
				return false;
		}	
	}
}