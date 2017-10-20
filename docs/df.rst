Data Flows
==========

Data flow diagrams (DFDs) are graphical models that model the flow of information (data flows) between external human or system actors external to the system (entities), activities that manipulate data (processes), and persistent data storage (data stores).
Together with attack trees.  In threat modelling, DFD model elements can be encompassed by *trust boundaries*; these occur where entities with different privileges interact.

Adding, updating, or deleting data flows
----------------------------------------

.. figure:: updateDataFlow.jpg
   :alt: Data Flow dialog


-   To add a data flow, select the UX / Data Flows menu to open the Data Flows table.  Click on the Add button to open a dialog for adding a new data flow.

-   Enter the name for the data flow, and select the environment the data flow is specific to.  You should also select the *from* and *to* types associated with the flow.  These types are Entities, Data Stores, and Processes, where Entities are information, hardware, or people assets, Data Stores are information assets, and Processes are use cases.

-   Click the Add button in the Asset table to choose one or more assets carried by this data flow.

-   Click on the Create button to add the data flow to the Data Flows table.

-   An existing data flow can be edited by clicking on a data flow in the Data Flow table, updating any aspect of the data flow, and clicking on the Update button.

-   Data flows can be deleted by clicking on the Delete button associated with the data flow to be removed in the Data Flows table.


Adding, updating, or deleting trust boundaries
----------------------------------------------

.. figure:: updateTrustBoundary.jpg
   :alt: Trust Boundary dialog

   -   To add a trust boundary, select the UX / Trust Boundaries menu to open the Trust Boundaries table.  Click on the Add button to open a dialog for adding a new trust boundary.

   -   Enter the name and a description for the trust boundary.

   -   Click on the Add button in the environment table, and select an environment to situate the trust boundary in. This will add the new environment to the environment list.

   -   Click the Add button in the Components table to situate a process or data store within this environment specific trust boundary.

   -   Click on the Create button to add the trust boundary to the Trust Boundary table.

   -   An existing trust boundary can be edited by clicking on a trust boundary in the Trust Boundaries table, updating any aspect of the trust boundary, and clicking on the Update button.

   -   Data flows can be deleted by clicking on the Delete button associated with the trust boundary to be removed in the Trust Boundaries table.


Viewing Data Flow Diagrams
--------------------------

DFDs can be viewed by selecting the Models/Data Flow menu, and selecting the environment to view the model for.

.. figure:: DFD.jpg
   :alt: DFD

By changing the environment name in the environment combo box, the DFD for a different environment can be viewed. The model can also be filtered by DFD model element.

By clicking on a model element, information about that artifact can be viewed.

For details on how to print DFDs as SVG files, see the `Generating Documentation`_ section.
