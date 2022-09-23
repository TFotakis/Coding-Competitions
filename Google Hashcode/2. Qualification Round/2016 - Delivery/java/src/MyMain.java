import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class MyMain {
	int rows, columns, turns, maxPayload;
	Warehouse[] warehouses;
	Drone[] drones;
	Order[] orders;
	int[] productsWeight;


	public static void main(String[] args) throws FileNotFoundException {
		MyMain m = new MyMain();
		m.runInputData("input/busy_day.in");
		m.runInputData("input/mother_of_all_warehouses.in");
		m.runInputData("input/redundancy.in");

	}

	public void runOrders(){

	}

	private void inputFileReader(String filename) throws FileNotFoundException{
		Scanner inputStream = new Scanner(new File(filename));
		rows=inputStream.nextInt();
		columns=inputStream.nextInt();
		drones=new Drone[inputStream.nextInt()];
		turns=inputStream.nextInt();
		maxPayload=inputStream.nextInt();
		inputStream.nextLine();
		productsWeight=new int[inputStream.nextInt()];
		inputStream.nextLine();
		for(int i=0;i<productsWeight.length;i++){
			productsWeight[i]=inputStream.nextInt();
		}
		inputStream.nextLine();
		warehouses = new Warehouse[inputStream.nextInt()];
		inputStream.nextLine();
		for(int i=0;i<warehouses.length;i++){
			int x=inputStream.nextInt();
			int y=inputStream.nextInt();
			inputStream.nextLine();
			int[] products = new int[inputStream.nextInt()];
			for(int j=0;j<products.length;j++){
				products[j]=inputStream.nextInt();
			}
			warehouses[i]=new Warehouse(x,y,products);
		}
		for(int i=0;i<drones.length;i++){
			drones[i]=new Drone(warehouses[0].x,warehouses[0].y,maxPayload);
		}
		inputStream.nextLine();
		orders=new Order[inputStream.nextInt()];
		for(int i=0;i<orders.length;i++){
			int x =inputStream.nextInt();
			int y =inputStream.nextInt();
			inputStream.nextLine();
			int[] products = new int[inputStream.nextInt()];
			for(int j=0;j<products.length;j++){
				products[j]=inputStream.nextInt();
			}
			orders[i] = new Order(x,y,products);
		}
		inputStream.close();
	}
	public void runInputData(String filename) throws FileNotFoundException
	{
		inputFileReader(filename);

	}

}
