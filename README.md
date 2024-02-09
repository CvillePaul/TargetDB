# TargetDB scientific astronomical database system

This project attempts to organize astronomical targets of scientific interest into a SQL database.  There should be no restrictions of what a *target* is - it could be a single star, an extended object, one or more gravitationally bound binary systems, etc.  Similarly, there is no restriction on the name given to a target - the name is called the Local ID and is meant to allow developments of a group's own catalog or naming scheme.

Each target can be associated with one or more other catalog objects, and the manor of the association is flexible.  For example, if a target comes directly from the TESS TIC catalog, the association would link to the TESS ID from that catalog and the nature of the association would be `Primary ID`.  Alternatively, if one were to do a cone search of Gaia DR3 objects near a given target, each row returned from that search would link to the corresponding Gaia DR3 ID and the association type might be `GAIA object within 2.0 arcsec`.

There are many types of data that can be linked to a target.  Tables exist to make entries for observations of the target's spectrum, and images using speckle interferometry, for example.  Beyond tracking this raw data, there is also the capability to associate one or more types of science result with a target.  Examples of science results include ephemerides determined for binary or multi-star systems, assessments of data quality of spectrum data, and results from resolving components of multi-star systems with speckle interferometry.

This work originated in service of the Quadruple Eclipsing Binaries research group (QuadEB), led by Steven Majewski at the University of Virginia.
