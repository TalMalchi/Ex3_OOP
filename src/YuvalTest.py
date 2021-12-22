# public NodeData center() {
#         try {
#             int minMaxKey = Integer.MAX_VALUE;
#             double minMaxValue = Double.MAX_VALUE;
#
#             Iterator<NodeData> itr = graph.nodeIter();
#             while (itr.hasNext())
#             { //for each node
#                 NodeData currNode = itr.next();
#                 HashMap<Integer, double[]> map = this.DijkstrasAlgo(currNode);
#                 double currMaxVal = 0;
#                 for (Map.Entry<Integer, double[]> entry : map.entrySet())
#                 { //for each entry in map
#                     if (currMaxVal < entry.getValue()[0])
#                     {
#                         currMaxVal = entry.getValue()[0];
#                     }
#                 }
#                 if (minMaxValue > currMaxVal)
#                 {
#                     minMaxKey = currNode.getKey();
#                     minMaxValue = currMaxVal;
#                 }
#             }
#             return this.graph.getNode(minMaxKey);
#         }
#         catch (Exception e) {
#             return null;
#         }
#     }