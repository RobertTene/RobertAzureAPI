from fastapi import APIRouter, HTTPException, Body
from typing import Annotated
from database import get_db_connection, create_db
import azure_services
from models import Order
from models import User


router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/create-user")
async def create_user(user: User):
    conn = get_db_connection()
    try:
        # Function to insert user into the database (to be defined in database.py)
        insert_user_into_db(conn, user)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/status/{id}")
async def status(id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM orders WHERE id = ?", (id,))
            order_status = cursor.fetchone()
            if order_status:
                return {"order_id": id, "status": order_status[0]}
            else:
                raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders")
async def get_orders():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
            return [{
                'id': order[0],
                'vm_name': order[1],
                'rg_name': order[2],
                'location': order[3],
                'user_id': order[4],
                'recipient_id': order[5],
                'status': order[6]
            } for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/makedb")
def makedb():
    create_db()


@router.post("/provision")
async def provision(order: Annotated[Order, Body(embed=True)]):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Insert order into the database
            query = '''
                INSERT INTO orders (vm_name, rg_name, location, user_id, recipient_id, status)
                VALUES (?, ?, ?, ?, ?, ?);
            '''
            values = (
            order.vm_name, order.resource_group, order.location, order.user_id, order.recipient_id, "creating")
            cursor.execute(query, values)
            order_id = cursor.lastrowid
            conn.commit()

            # Provision Azure resources
            try:
                # Example Azure service calls
                # Replace with actual logic for provisioning VMs, NICs, etc.
                azure_services.create_vnet(order.resource_group, order.location, "vnet_name")
                subnet = azure_services.create_subnet(order.resource_group, "vnet_name", "subnet_address")
                public_ip = azure_services.create_public_ip(order.resource_group, order.location)
                nic = azure_services.create_nic(order.resource_group, order.location, public_ip.id, subnet.id)
                vm = azure_services.create_vm(order.resource_group, order.location, order.vm_name, nic.id)

                # Update order status to 'provisioned' after successful Azure operations
                update_status_query = 'UPDATE orders SET status = ? WHERE id = ?'
                cursor.execute(update_status_query, ("provisioned", order_id))
                conn.commit()
            except Exception as e:
                # Handle Azure provisioning errors
                # Log the error and update order status to 'error'
                print(f"Error during Azure provisioning: {e}")
                cursor.execute('UPDATE orders SET status = ? WHERE id = ?', ("error", order_id))
                conn.commit()
                raise HTTPException(status_code=500, detail="Error in Azure provisioning")

            return {"order_id": order_id, "status": "provisioned"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

