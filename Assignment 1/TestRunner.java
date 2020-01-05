//RED ID: 824654344
//[TestRunner.java]
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

//Class for implementing the test cases written in TestCircularDoublyLinkedQueue.java
public class TestRunner 
{
	public static void main(String[] args) 
	{
		Result result = JUnitCore.runClasses(TestCircularDoublyLinkedQueue.class);
	
		for (Failure failure : result.getFailures()) 
		{
			System.out.println(failure.toString());
		}
		
		System.out.println(result.wasSuccessful());
	}
}