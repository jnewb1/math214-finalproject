class Node
{
    bool infected = false;
};

class Edge
{
    Node *node1;
    Node *node2;

    Edge(Node *node1_in, Node *node2_in)
    {
        node1 = node1_in;
        node2 = node2_in;
    }
};