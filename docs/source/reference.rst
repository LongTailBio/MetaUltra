



The .mu folder
--------------

- .mu/mudb the mu database



mu init
-------

- Make .mu folder in current directory



Running and results
-------------------

A result is fully defined by a module, a data-record, and a conf.

Explanation:

- A data-record defines the underlying files used to generate the result as well as a data-type.
- A module defines its expected output given a data-type.
- A conf describes the parameters with which a module was run.

Pipelines can be run given a set of data-records (all of the same data-type) and a conf.
This is because:

- Confs specify which modules should be run
- Modules are aware of how to handle different data-types (No action is a valid handling)

Modules are not aware of their corresponding pipeline implementation. This means that if
a module's pipeline implementation is changed a corresponding result will be unaware. This
behaviour is acceptable because:

- Total file provenance is not a goal of MetaUltra
- Most changes to a module's pipeline are likely to be bugfixes or changes to
  operational parameters
- Major changes to a module's pipeline should be accompanied by removal of the
  corresponding files. This will send results into an error state from which they
  can be corralled and removed from the mudb

Module versioning can be accomplished by building an entirely new module. This is
acceptable because modules are presumed to roughly correspond to software versions.
