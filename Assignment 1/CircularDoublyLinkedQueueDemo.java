//Author: Dhaval Harish Sharma
//RED ID: 824654344
//Currently enrolled in the class
/*Assignment 1: Implementing a circular doubly linked queue with a support for adding and deleting elements with O(1) time complexity. The queue begins with a capacity of 2 which increases when we try to add element in a fully filled queue. The queue holds process objects which contains name, owner, PID, number of threads, percent of CPU currently used and total amount of CPU time used. The elements are removed from the queue ordered by name, PID, number of threads, percent of CPU currently used, total amount of CPU time used and owner*/
//Version: 1.0

//[CircularDoublyLinkedQueueDemo.java]
import java.util.*;

//Class for implementing the main function of CircularDoublyLinkedQueue class
class CircularDoublyLinkedQueueDemo
{
	public static void main(String[] args)
	{
		Scanner scannerObj = new Scanner(System.in);
		char choice;
		int operation;
		
		//Initializing the Circular Doubly Linked Queue with 2 capacity
		CircularDoublyLinkedQueue cdlqObj = new CircularDoublyLinkedQueue();
		cdlqObj.addEmptyNode();
		cdlqObj.addEmptyNode();

		//Loop for taking inputs from the user till he presses "N"
		do
		{
			System.out.println("Enter the operation:");
			System.out.println("(1) Display the circular doubly linked queue.");
			System.out.println("(2) Display element by attribute.");
			System.out.println("(3) Insert an element to the queue.");
			System.out.println("(4) Delete an element from the queue.");
			
			try
			{
				operation = scannerObj.nextInt();
				
				switch(operation)
				{
					//Display the circular doubly linked queue using displayQueue function
					case 1:
						cdlqObj.displayQueue();
						System.out.println("\nThe current capacity of the queue is " + cdlqObj.capacity);
						break;
					
					//Display the circular doubly linked queue by attributes using displaySortedQueue function
					case 2:
						System.out.println("Enter the attribute to sort:");
						System.out.println("[Available choices = PID, Name, Owner, NumOfThreads, CPUPercent, CPUTime]");
						String selectedAttribute = scannerObj.next();
						cdlqObj.displaySortedQueue(selectedAttribute);
						break;
						
					//Insert an element at the end of the circular doubly linked queue using addElement function
					case 3:
						Process newProcess = new Process();
						newProcess.setProcessAttributes();
						cdlqObj.addElement(newProcess);
						break;
						
					//Delete the first element from the circular doubly linked queue using removeElement function
					case 4:
						Process removedElement = new Process();
						removedElement = cdlqObj.removeElement();
						if(removedElement != null)
						{
							System.out.println("\nThe removed element is:");
							removedElement.displayProcessAttributes();
						}
						else
						{
							System.out.println("The queue contains no elements!");
						}
						break;
						
					//Invalid input from the user
					default:
						System.out.println("Oops! You entered wrong operation. Please try again..");
						break;
				}
			}
			catch(Exception catchedException)
			{
				System.out.println("Oops! You entered wrong value. Please try again..");
			}
			
			System.out.println("\nDo you want to continue?");
			System.out.println("Press Y for Yes and N for No.");
			choice = scannerObj.next().charAt(0);
		}while(choice == 'Y' || choice == 'y');
	}
}