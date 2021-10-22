'use strict'

const bodyParser = require('body-parser')
const { request, gql } = require('graphql-request')

module.exports = ({ app }, wrap) => {
  app.use(bodyParser.json())
  app.post('/', wrap(handler))
}

const handler = async input => {
  const id = input.id
  const endpoint = process.env.GRAPHQL_ENDPOINT

  const mutation = gql`
    mutation UpdateTodo($id: uuid!) {
      update_todos_by_pk(_set:{
        state: DOING
      }, pk_columns: {
        id: $id
      }) {
        id
      }
    }
  `

  await request(endpoint, mutation, { id })

  const result = {
    state: 'DOING'
  }

  return result
}