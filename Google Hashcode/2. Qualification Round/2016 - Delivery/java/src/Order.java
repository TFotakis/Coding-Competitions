public class Order {
	public int x,y, totalOrderWeight = 0;
	public int[] products;
	public boolean completed;
	
	Order(int x,int y, int[] products){
		this.x=x;
		this.y=y;
		this.products=products;
	}
	
	public int findWeight()
	{
		for (int i = 0; i<products.length;i++)
		{
			totalOrderWeight += products[i];
		}
		return totalOrderWeight;
	}
	
	public void setWarehouses(Warehouse[] wa)
	{
		
	}
	
}
