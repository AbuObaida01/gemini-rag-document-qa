function Answer({ result }) {
    if (!result) {
      return null;
    }
  
    return (
      <section className="card">
        <h2>Answer</h2>
  
        <div className="answer">
          {result.answer}
        </div>
      </section>
    );
  }
  
  export default Answer;