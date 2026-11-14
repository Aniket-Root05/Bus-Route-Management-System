from collections import deque
BUS_NETWORK = {
    "Durg": {"Bhilai": 10, "Raipur": 40, "Rajnandgaon": 45},
    "Bhilai": {"Durg": 10, "Raipur": 30},
    "Raipur": {"Bhilai": 30, "Durg": 40, "Bilaspur": 110, "Dhamtari": 80},
    "Bilaspur": {"Raipur": 110},
    "Dhamtari": {"Raipur": 80},
    "Rajnandgaon": {"Durg": 45},
    "Jagdalpur": {"Kondagaon": 75},
    "Kondagaon": {"Jagdalpur": 75}
}

FARE_PER_KM = 1.50


def find_stop_name(user_input):
    """Matches user input case-insensitively to the canonical stop name in BUS_NETWORK."""
    cleaned = user_input.strip().lower()
    for stop in BUS_NETWORK:
        if stop.lower() == cleaned:
            return stop
    return None


def show_connections(stop_input):
    """Displays all direct neighbouring stops and distances for a chosen stop."""
    stop = find_stop_name(stop_input)
    if not stop:
        print(f"Stop '{stop_input.strip()}' not found.")
        return

    neighbours = BUS_NETWORK[stop]
    connections_list = [f"{neighbour} ({dist} km)" for neighbour, dist in neighbours.items()]
    print(f"{stop} connects to: {', '.join(connections_list)}")


def find_route_bfs(start_input, end_input):
    """Finds the route with the fewest stops between two stops using Breadth-First Search (BFS)."""
    start = find_stop_name(start_input)
    end = find_stop_name(end_input)

    if not start:
        print(f"Stop '{start_input.strip()}' not found.")
        return
    if not end:
        print(f"Stop '{end_input.strip()}' not found.")
        return

    if start == end:
        print("Source and destination are the same. Distance: 0 km.")
        print("Fare: Rs. 0.00")
        return

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current_stop, path = queue.popleft()

        for neighbour in BUS_NETWORK[current_stop]:
            if neighbour == end:
                full_path = path + [neighbour]
                total_distance = sum(
                    BUS_NETWORK[full_path[i]][full_path[i + 1]]
                    for i in range(len(full_path) - 1)
                )
                total_fare = total_distance * FARE_PER_KM
                print(f"Route: {' -> '.join(full_path)}")
                print(f"Stops: {len(full_path)} | Distance: {total_distance} km | Fare: Rs. {total_fare:.2f}")
                return

            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    print(f"No route available between {start} and {end}.")


def main():
    while True:
        print("\n--- Bus Route Management System ---")
        print("1. Show connections")
        print("2. Find route")
        print("3. Exit")
        choice = input("Menu: ").strip().lower()

        if choice in ("1", "show connections"):
            stop_name = input("Stop: ")
            show_connections(stop_name)
        elif choice in ("2", "find route"):
            source = input("From: ")
            destination = input("To: ")
            find_route_bfs(source, destination)
        elif choice in ("3", "exit"):
            print("Exiting Bus Route Management System.")
            break
        else:
            print("Invalid menu choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()