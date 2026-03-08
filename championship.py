from urllib.request import urlopen
import json
import math
class Driver:
    def __init__(self, number, name, team):
        self.number = number
        self.name = name
        self.team = team
        self.points = 0
        self.position = 0

    def __str__(self):
        return self.name
    
    def update_standing(self, points, position):
        self.points = points or 0
        self.position = position or 0

class Team:
    def __init__(self, name):
        self.name = name or "Unknown"
        self.points = 0
        self.position = 0


    def __str__(self):
        return f"{self.position:<3} | {self.name:<20} | {self.points:>5.1f} pts"

    def update_standing(self, points, position):
        self.points = points or 0
        self.position = position or 0

class Championship:

    base_url = 'https://api.openf1.org/v1'

    def __init__(self):
        self.drivers = {}
        self.teams = {}
        self.gps = {
            "Melbourne": math.ceil(305 / 5.278), #TODO Criar a lista de gps
            "Shanghai": math.ceil(305 / 5.451)
        }

    def _fetch_json(self, endpoint):
        url = f"{self.base_url}/{endpoint}?session_key=latest"
        with urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))

    def _fetch_json_laptimes(self, laps, driver_number, lap):
        url = f"{self.base_url}/{laps}?session_key=latest&driver_number={driver_number}&lap_number={lap}"
        with urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))

    def sync_data(self):
        try:
            drivers_data = self._fetch_json('drivers')
            drivers_standings_data = self._fetch_json('championship_drivers')
            teams_standings_data = self._fetch_json('championship_teams')

            # Adds drivers to self.drivers
            for entry in drivers_data:
                num = entry['driver_number']

                if num is not None and num not in self.drivers:
                    self.drivers[num] = Driver(
                        number=num,
                        name = entry.get('broadcast_name', 'Unknown'),
                        team=entry.get('team_name', "N/A")
                    )
            
            # Update Drivers Standings
            for entry in drivers_standings_data:
                num = entry['driver_number']
                if num in self.drivers:
                    self.drivers[num].update_standing(
                        points=entry.get('points_current', 0),
                        position=entry.get('position_current', 0)
                    )

            # Adds teams to self.teams and update Teams Standings
            for entry in teams_standings_data:
                name = entry.get('team_name') or f"Unknown Team ({entry.get('position_current')})"

                if not name:
                    continue
                
                if name not in self.teams:
                    self.teams[name] = Team(name=name)
                
                self.teams[name].update_standing(
                    points=entry.get('points_current', 0) or 0,
                    position=entry.get('position_current', 0) or 0
                )
                        
        except Exception as e:
            print(f"Error syncing with OpenF1.org: {e}")

    def getDriver(self, driver_number):
        return self.drivers.get(driver_number)

    def getDrivers(self):
        list_drivers = []

        for driver_obj in self.drivers.values():
            list_drivers.append(driver_obj.name)
        
        return sorted(list_drivers)
    
    def getDriversSortedByPoints(self):
        list_drivers = []
        sorted_drivers = sorted(
            self.drivers.values(),
            key=lambda x: (x.position == 0, x.position)
        )
        list_drivers = sorted_drivers

        return list_drivers
    
    def getTeamsSortedByPoints(self):
        list_teams = []
        sorted_teams = sorted(
            self.teams.values(),
            key = lambda x: (x.position == 0, x.position)
        )
        list_teams = sorted_teams
        return list_teams

    def compare_drivers_laps(self, driver1_number, driver2_number, lap):
        driver1 = f1.getDriver(driver1_number)
        driver2 = f1.getDriver(driver2_number)
        driver1_laps = f1._fetch_json_laptimes("laps", driver1_number, lap)
        driver2_laps = f1._fetch_json_laptimes("laps", driver2_number, lap)



if __name__ == "__main__":
    f1 = Championship()
    f1.sync_data()