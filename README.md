## Initialization

```console
    yarprobotinterface --context simCartesianControl --config no_legs.xml
    iKinCartesianSolver --context simCartesianControl --part left_arm
    iKinCartesianSolver --context simCartesianControl --part right_arm
```

## Execution

```console
    python example.py
```