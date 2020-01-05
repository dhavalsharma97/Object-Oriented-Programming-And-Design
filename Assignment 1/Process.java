//RED ID: 824654344
//[Process.java]
import java.util.*;

//Class for implementing the process elements which are to be added to the nodes of circular doubly linked queue
class Process
{
	protected int pid;
	protected String name;
	protected String owner;
	protected int numOfThreads;
	protected int cpuPercent;
	protected int cpuTime;
	
	//Default constructor for initializing the fields of class Process
	public Process()
	{
		pid = 0;
		name = null;
		owner = null;
		numOfThreads = 0;
		cpuPercent = 0;
		cpuTime = 0;
	}
	
	//Function for initializing the fields of class Process
	public void setProcessAttributes()
	{
		Scanner scannerObj = new Scanner(System.in);
		
		System.out.println("\nEnter the following details of process:");
		System.out.print("The PID of process: ");
		pid = scannerObj.nextInt();
		System.out.print("The name of process: ");
		name = scannerObj.next();
		System.out.print("The owner of process: ");
		owner = scannerObj.next();
		System.out.print("The number of threads in the process: ");
		numOfThreads = scannerObj.nextInt();
		System.out.print("The percent of cpu used by process: ");
		cpuPercent = scannerObj.nextInt();
		System.out.print("The cpu time used by process: ");
		cpuTime = scannerObj.nextInt();
	}
	
	//Overloaded function for initializing the fields of class Process
	public void setProcessAttributes(int newPID, String newName, String newOwner, int newNumOfThreads, int newCpuPercent,
	int newCpuTime)
	{
		pid = newPID;
		name = newName;
		owner = newOwner;
		numOfThreads = newNumOfThreads;
		cpuPercent = newCpuPercent;
		cpuTime = newCpuTime;
	}
	
	//Function for displaying the fields of class Process
	public void displayProcessAttributes()
	{
		System.out.println("The PID of process: " + pid);
		System.out.println("The name of process: " + name);
		System.out.println("The owner of process: " + owner);
		System.out.println("The number of threads in the process: " + numOfThreads);
		System.out.println("The percent of cpu used by process: " + cpuPercent);
		System.out.println("The cpu time used by process: " + cpuTime);
	}
}