//compile: g++ omplapp_test.cpp -L/usr/local/lib -lompl -lompl_app -lompl_app_base -o omplapp_test.run -std=c++11

#include <omplapp/apps/SE3RigidBodyPlanning.h>
#include <omplapp/config.h>
#include "env_set.h"

using namespace ompl;

int main(){
	app::SE3RigidBodyPlanning setup;
	//std::string robot_fname = "/home/shin-u16/tools/omplapp-1.3.1-Source/resources/3D/Easy_robot.dae";
	//std::string env_fname = "/home/shin-u16/tools/omplapp-1.3.1-Source/resources/3D/Easy_env.dae";
	
	std::string robot_fname = std::string(OMPLAPP_RESOURCE_DIR) + std::string(ENV);
	std::string env_fname = std::string(OMPLAPP_RESOURCE_DIR) + std::string(ROBOT);

	setup.setRobotMesh(robot_fname);
	setup.setEnvironmentMesh(env_fname);

	base::ScopedState<base::SE3StateSpace> start(setup.getSpaceInformation());
	start->setX(START_X);
	start->setY(START_Y);
	start->setZ(START_Z);
	start->rotation().setIdentity();

	base::ScopedState<base::SE3StateSpace> goal(start);
	goal->setX(END_X);
	goal->setY(END_Y);
	goal->setZ(END_Z);
	goal->rotation().setIdentity();

	setup.setStartAndGoalStates(start, goal);
	setup.getSpaceInformation()->setStateValidityCheckingResolution(0.01);
	setup.setup();
	setup.print();

	if (setup.solve(10)){
		setup.simplifySolution();
		setup.getSolutionPath().printAsMatrix(std::cout);
	}

	return 0;
}
