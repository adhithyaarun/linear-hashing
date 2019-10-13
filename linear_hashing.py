import sys
import os


class Linear_Hashing:
    def __init__(self):
        """Initialize Class Variables"""
        self.hash_table = {}  	# Hash Table
        self.split_pointer = 0  # Split pointer
        self.capacity = 1024    # Size of a bucket (in bytes)
        self.total_blocks = 2   # Total Number of blocks in the Hash Table
        self.bucket_count = 2   # Number of buckets
        self.uniques = 0        # Number of unique values
        self.curr_mod = 2       # Current mod value
        self.next_mod = 4       # Next mod value (2 * curr)
        self.block_count = {}  	# Number of blocks per key (faster than len())

        # Block counts initialized to 1
        self.block_count[0] = 1
        self.block_count[1] = 1

    def insert(self, value):
        """Insert new value into Hash Table if not already present"""
        found = False
        key = value % self.curr_mod

        # Check if h(i+1) is being used
        if key < self.split_pointer:
            key = value % self.next_mod

        # Check if new bucket used
        if key not in self.hash_table:
            self.hash_table[key] = [[]]

        # Search for value
        for i in range(self.block_count[key]):
            if value in self.hash_table[key][i]:
                found = True

        # If value not found, insert into hash table
        if found is not True:
            self.uniques += 1         	 	   # Increment number of unique values added
            index = self.block_count[key] - 1  # Get last index for the key

            # NOTE: Multiply by 4 to account for 4 bytes per integer
            if 4 * len(self.hash_table[key][index]) >= self.capacity:
                self.hash_table[key].append([])
                self.total_blocks += 1
                self.block_count[key] += 1
                index += 1

            # Insert value into Hash Table
            self.hash_table[key][index].append(value)

            # Print new value
            print(value)

        # Check if new buckets are required (based on occupancy)
        if self.check_treshold():
            self.create_bucket()

    def check_treshold(self):
        """Check the occupancy and indicate high/low occupancy"""
        density = (4.0 * self.uniques) / (self.capacity * self.total_blocks)
        # Note the above 4 is assuming 4 bytes per number
        # If occupancy/density of values is more than 75%, add new buckets
        if density > 0.75:
            return True
        return False

    def create_bucket(self):
        """Create new bucket for the bucket at the split pointer"""
        temp_array = []        	# Temporary array to hold data from split bucket
        self.bucket_count += 1

        # Transfer values from the bucket to temporary array
        for i in range(self.block_count[self.split_pointer]):
            for value in self.hash_table[self.split_pointer][i]:
                temp_array.append(value)

        # Removing all values in bucket
        self.total_blocks -= self.block_count[self.split_pointer]
        self.hash_table[self.split_pointer] = [[]]   # Clearing old bucket
        self.block_count[self.split_pointer] = 1     # Resetting count
        self.total_blocks += 1                       # Update total_blocks

        # Initializing new bucket
        self.hash_table[self.bucket_count - 1] = [[]]
        self.block_count[self.bucket_count - 1] = 1  # Initializing count
        self.total_blocks += 1                       # Update total_blocks

        # Re-insert all values into the Hash Table
        for value in temp_array:
            found = False
            key = value % self.next_mod

            # Check if new bucket used
            if key not in self.hash_table:
                self.hash_table[key] = [[]]
                self.block_count[key] = 1
                self.total_blocks += 1

            # Search for value
            for i in range(self.block_count[key]):
                if value in self.hash_table[key][i]:
                    found = True

                # If value not found, insert into hash table
            if not found:
                # Get last index for the key
                index = self.block_count[key] - 1

                # NOTE: Multiply by 4 to account for 4 bytes per integer
                if 4 * len(self.hash_table[key][index]) >= self.capacity:
                    self.hash_table[key].append([])
                    self.total_blocks += 1
                    self.block_count[key] += 1
                    index += 1

                    # Insert value into Hash Table
                self.hash_table[key][index].append(value)

        # Push split pointer to next index
        self.split_pointer += 1

        # If number of buckets is same as next_mod,
        # then split pointer has reached the end.
        # Hence, update curr_mod & next_mod and reset split pointer.
        if self.bucket_count == self.next_mod:
            self.curr_mod = self.next_mod
            self.next_mod = self.curr_mod * 2
            self.split_pointer = 0


if __name__ == "__main__":
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print("File not found.")
        exit(1)

    hashing = Linear_Hashing()

    with open(filename) as file:
        for line in file:
            value = int(line.strip())
            hashing.insert(value)
