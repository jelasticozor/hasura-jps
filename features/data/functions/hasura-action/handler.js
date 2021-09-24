'use strict'

const { request, gql } = require('graphql-request')

module.exports = async (event, context) => {
  const id = event.body.input.id
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

  try
  {
    const data = await request(endpoint, mutation, { id })

    const result = {
      state: 'DOING'
    }

    return context
      .status(200)
      .succeed(result)
  }
  catch(err)
  {
    return context
      .status(400)
      .succeed({
        "message": err
      })
  }
}