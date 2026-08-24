function SourceList({ sources }) {
    if (!sources || sources.length === 0) {
      return null;
    }
  
    return (
      <section className="card">
        <h2>Sources</h2>
  
        <div className="source-list">
          {sources.map((source, index) => (
            <div
              className="source-item"
              key={`${source.document}-${source.chunk}-${index}`}
            >
              <strong>
                {source.document}
              </strong>
  
              <span>
                Page: {source.page}
              </span>
  
              <span>
                Chunk: {source.chunk}
              </span>
  
              <span>
                Distance:{" "}
                {Number(
                  source.distance
                ).toFixed(4)}
              </span>
            </div>
          ))}
        </div>
      </section>
    );
  }
  
  export default SourceList;