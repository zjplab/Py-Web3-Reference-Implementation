import hashlib
import json

def hash_data(data):
    """Create a SHA-256 hash of the given data."""
    data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self):
        self.tree = []

    def build_tree(self, leaf_nodes):
        """Build the Merkle tree from the given leaf nodes."""
        self.tree = [leaf_nodes]

        while len(self.tree[-1]) > 1:
            current_layer = self.tree[-1]
            next_layer = []

            for i in range(0, len(current_layer), 2):
                if i+1 < len(current_layer):
                    next_node = hash_data(current_layer[i] + current_layer[i+1])
                    next_layer.append(next_node)
                else:
                    # If there is an odd number of nodes, hash the last node again
                    next_node = hash_data(current_layer[i] + current_layer[i])
                    next_layer.append(next_node)

            self.tree.append(next_layer)

    def get_root(self):
        """Get the root of the Merkle tree."""
        return self.tree[-1][0] if self.tree else None

    def update_leaf(self, leaf_index, new_value):
        """Update a leaf node and recalculate the necessary hashes."""
        if leaf_index >= len(self.tree[0]):
            raise IndexError("Leaf index is out of bounds")

        # Update the leaf node
        self.tree[0][leaf_index] = hash_data(new_value)

        # Recalculate hashes
        for i in range(1, len(self.tree)):
            node_index = leaf_index // (2 ** i)
            sibling_index = node_index ^ 1

            # Check if this is a right or left node
            if node_index * 2 + 1 >= len(self.tree[i - 1]):
                # This is a rightmost node, so we hash it with itself
                self.tree[i][node_index] = hash_data(self.tree[i - 1][node_index * 2])
            elif node_index % 2 == 0:
                # This is a left node, so we hash it with its right sibling
                self.tree[i][node_index] = hash_data(
                    self.tree[i - 1][node_index * 2] + self.tree[i - 1][node_index * 2 + 1]
                )
            else:
                # This is a right node, so we hash it with its left sibling
                self.tree[i][node_index] = hash_data(
                    self.tree[i - 1][sibling_index * 2] + self.tree[i - 1][node_index * 2]
                )
def main():
    # Create some leaf nodes
    leaf_nodes = ['data1', 'data2', 'data3', 'data4']
    hashed_leaf_nodes = [hash_data(leaf) for leaf in leaf_nodes]
    
    # Create and build the Merkle tree
    merkle_tree = MerkleTree()
    merkle_tree.build_tree(hashed_leaf_nodes)
    
    # Print the Merkle root
    original_root = merkle_tree.get_root()
    print("Original Merkle root:", original_root)
    
    # Now let's change a leaf node
    merkle_tree.update_leaf(0, 'new_data1')
    
    # Print the Merkle root again
    updated_root = merkle_tree.get_root()
    print("Updated Merkle root:", updated_root)
    
    # Make sure the root has changed
    assert original_root != updated_root, "Merkle roots are the same after update!"
    
    # Now change the leaf node back to its original value
    merkle_tree.update_leaf(0, 'data1')
    
    # Print the Merkle root again
    reverted_root = merkle_tree.get_root()
    print("Reverted Merkle root:", reverted_root)
    
    # Make sure the root is back to its original value
    assert original_root == reverted_root, "Merkle roots are different after reverting update!"
    
    print("All tests passed!")

if __name__ == "__main__":
  main()
