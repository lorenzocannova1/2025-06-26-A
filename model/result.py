from dataclasses import dataclass


@dataclass

class Result:
    driverId: int
    position: int

    def __eq__(self, other):
        return self.driverId == other.driverId
    def __hash__(self):
        return hash(self.driverId)
    def __str__(self):
        return f"{self.driverId}"