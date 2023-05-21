const cassandra = require('cassandra-driver');

// Connect to the Cassandra cluster
const client = new cassandra.Client({
  contactPoints: ['127.0.0.1'], // Replace with your cluster's contact points
  localDataCenter: 'test', // Replace with your cluster's data center
  keyspace: 'my_keyspace' // Replace with your keyspace name
});

// Execute a query to retrieve data from a table
const query = "SELECT * FROM test.power WHERE home_id='CDB004'";
// You don't need params in this case, since there are no query parameters

client.execute(query, { prepare: true })
  .then(result => {
    console.log('Retrieved data:', result.rows);
    // Process the retrieved data as needed 
  })
  .catch(error => {
    console.error('Error retrieving data:', error);
  })
  .finally(() => {
    // Close the client connection when done
    client.shutdown();
  });
