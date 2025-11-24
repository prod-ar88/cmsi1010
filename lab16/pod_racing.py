from dataclasses import dataclass
from typing import Callable
import matplotlib.pyplot as plt
import math


@dataclass
class Pod:
    name: str
    velocity_at: Callable[[float], float]

    def trajectory(self, total_time, dt):
        distance = 0
        points = [(0, 0)]
        for t in range(0, total_time, dt):
            v_t = self.velocity_at(t)
            v_t_plus_dt = self.velocity_at(t + dt)
            distance += ((v_t + v_t_plus_dt) / 2) * dt
            points.append((t + dt, distance))
        return points


racers = [
    Pod("Solid Performer", lambda t: t if t < 20 else 20),
    Pod("Slow Starter", lambda t: 0 if t < 30 else min(25, (t - 30) / 2)),
    Pod("To Infinity and Beyond", lambda t: t * 0.75),
    Pod("Jerky", lambda t: 15 if (t // 10) % 2 == 0 else -5),
    Pod("Cheetah", lambda t: t * 3),
    Pod("Snails A Lot", lambda t: 0 if t < 10 else min(5, (t - 10) / 5)),
    Pod("Mr. Meh", lambda t: 500 if (t // 15) % 5 == 0 else -10),
    Pod("QWERTY", lambda t: 250 * math.tan((40 / math.pi) * t)),
    Pod("Devil Jr.", lambda t: 900 * math.sin((700 / 50) * t)),
    Pod("AAAAAAA!", lambda t: 5000 * math.cos((2000 / math.pi) * t)),
    Pod("Fractal Fury", lambda t: 2000 * math.sin(0.5 * t * t) * math.cos(3 * t)),
    Pod("Broken Mirror", lambda t: 100 *
        math.sin(t) / max(0.01, math.cos(t / 7))),
    Pod("Rampage Reactor", lambda t: min(1050, 50 * math.exp(t / 20)))
]


def print_trajectories(pods, total_time, dt):
    for pod in pods:
        print(f"Trajectory for {pod.name}:")
        for t, d in pod.trajectory(total_time, dt):
            print(f"  At t={t}s: {d}m")
        print()


def plot_trajectories(pods, total_time, dt):
    plt.figure(figsize=(10, 6))
    for pod in pods:
        times, distances = zip(*pod.trajectory(total_time, dt))
        plt.plot(times, distances, label=pod.name)
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.title("Pod Racing Trajectories")
    plt.legend()
    plt.grid()
    plt.show()


plot_trajectories(racers, total_time=120, dt=5)
