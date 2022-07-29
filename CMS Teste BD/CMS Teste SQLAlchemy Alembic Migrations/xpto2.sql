-- Running downgrade c357afe11b1c -> eada2cf7f14f

ALTER TABLE pessoa2 DROP COLUMN idade;

UPDATE alembic_version SET version_num='eada2cf7f14f' WHERE alembic_version.version_num = 'c357afe11b1c';

-- Running downgrade eada2cf7f14f -> e6a1748a3b5a

DROP TABLE pessoa2;

UPDATE alembic_version SET version_num='e6a1748a3b5a' WHERE alembic_version.version_num = 'eada2cf7f14f';

