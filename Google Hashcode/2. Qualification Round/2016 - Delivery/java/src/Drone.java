public class Drone {
	public int x,y, goX, goY;
	public int turns;
	public int maxLoadWeight;
	public int currentLoadWeight = 0;
	public boolean inWareHouse = true;
	public boolean toWareHouse = false;
	public boolean onMission = false;
	
	
	Drone(int x, int y, int maxWeight){
		this.x=x;
		this.y=y;
		maxLoadWeight = maxWeight;
		turns=0;
	}
	
	public void loadDrone(Order or){
		if(maxLoadWeight>=or.totalOrderWeight)
		{
			onMission = true;
			goX = or.x;
			goY = or.y;
			currentLoadWeight += or.totalOrderWeight;
		}
	}
	
}
