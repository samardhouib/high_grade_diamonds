// MongoDB initialization script
db = db.getSiblingDB('e_shop');

// Create user for the application
db.createUser({
  user: 'admin',
  pwd: 'secret123',
  roles: [
    {
      role: 'readWrite',
      db: 'e_shop'
    }
  ]
});

print('MongoDB initialized with e_shop database and user.');'
