// Initialize database constraints and indexes for AiON

// Ensure Project IDs are unique
CREATE CONSTRAINT project_id IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE;

// Ensure Decision IDs are unique
CREATE CONSTRAINT decision_id IF NOT EXISTS FOR (d:Decision) REQUIRE d.id IS UNIQUE;

// Ensure Module names are unique
CREATE CONSTRAINT module_name IF NOT EXISTS FOR (m:Module) REQUIRE m.name IS UNIQUE;

// Ensure Technology names are unique
CREATE CONSTRAINT tech_name IF NOT EXISTS FOR (t:Tech) REQUIRE t.name IS UNIQUE;
