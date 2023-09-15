import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";


function FlowcellsID() {


    const { id } = useParams()

    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ flowcell_info, setFlowcellInfo ] = useState(null);
      
    useEffect(() => {
        fetch(`/flowcells/${id}`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setFlowcellInfo(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])// eslint-disable-line react-hooks/exhaustive-deps

    console.log("Flowcell ", id, " content :",flowcell_info)
    
    let body = <></>;
    let head = <></>;
    
    if (error) {
        return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Loading...</div>;
    } else {
        


        head = (
        <thead>
          <tr>
            <th>№</th>
            <th>Образец</th>
            <th>Реплика</th>
          </tr>
        </thead>);

        body = (
            <tbody>
            {flowcell_info.biosamples.map((biosample, index) => {
                return (
                    <tr key={index}>
                    <th>{index + 1}</th>
                    <th>
                    <Link to={`/biosamples/${biosample.biosample_name}`}>
                        <b>{biosample.biosample_name}</b>
                    </Link>
                    </th>
                    <th>
                        {biosample.replica}
                    </th>
                    </tr>
                );
            })
            }
            </tbody>
        );

    }
    return (
        <><Card>
        <Table bordered hover>
            {head}
            {body}

        </Table>
        
        </Card></>
    )
}

//
//    return (
//        <>
//        <Card>
//        <h4
//            style={{
//                marginTop: 25,
//                marginBot: 25,
//                marginLeft: 25,
//                marginRight: 25,
//            }}>
//        
//        Проект :<b> {id}</b>
//        </h4>
//        </Card>
//
//        <Card>
//        <Table bordered hover>
//            {head}
//            {body}
//        </Table>
//        
//        </Card>
//      </>
//      
//    );
//    
//}    
export default FlowcellsID;
