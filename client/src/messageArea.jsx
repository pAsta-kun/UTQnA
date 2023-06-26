import './App.css'
const user = {
    name: 'Ali',
    favColor: '#6d5af1'
}
function TextBubble({isAI, text}) {
    
    if(isAI)
    {
        return (
            <>
                <div className="textArea ai">
                    <div className="userInfo">
                        <h3 className="userIcon aiIcon"></h3>
                        <h3 className="username">AO</h3>
                    </div>
                    <div className="message" style={{ whiteSpace: 'pre-wrap' }}>{text}</div>
                </div>
            </>
        )
    }
    else return(
        <>
            <div className="textArea">
                <div className="userInfo">
                    <h3 className="userIcon" style={{background: user.favColor}}></h3>
                    <h3 className="username">{user.name}</h3>
                </div>
                <div style={{ whiteSpace: 'pre-wrap' }} className="message">{text}</div>
            </div>
        </>
        
    )

}

export default TextBubble
