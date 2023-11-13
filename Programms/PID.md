```mermaid
  graph TD;
      Input -->P;
      Input -->I;
      Input -->D;
      P ->>Motor;
      I ->>Motor;
      D ->>Motor;
      Motor -->Sensor;
      Sensor --> Input
```
